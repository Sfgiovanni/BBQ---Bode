#!/usr/bin/env bash
set -Eeuo pipefail

readonly REPOSITORY_URL="https://github.com/Sfgiovanni/BBQ---Bode.git"
readonly REPOSITORY_PAGE="https://github.com/Sfgiovanni/BBQ---Bode"
readonly REMOTE_NAME="publication"
readonly TARGET_BRANCH="${TARGET_BRANCH:-main}"
readonly DEFAULT_MESSAGE="Publish reproducible bilingual BBQ-Bode benchmark"

ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")/.." rev-parse --show-toplevel 2>/dev/null)" || {
  echo "Erro: execute este script dentro do repositorio BBQ-Bode." >&2
  exit 1
}
cd "$ROOT"

ASKPASS_FILE=""
GITHUB_TOKEN=""

cleanup() {
  GITHUB_TOKEN=""
  unset GITHUB_TOKEN
  if [[ -n "$ASKPASS_FILE" && -f "$ASKPASS_FILE" ]]; then
    rm -f -- "$ASKPASS_FILE"
  fi
}
trap cleanup EXIT INT TERM

fail() {
  echo "Erro: $*" >&2
  exit 1
}

for command in git mktemp paste; do
  command -v "$command" >/dev/null 2>&1 || fail "comando obrigatorio nao encontrado: $command"
done

git check-ref-format --branch "$TARGET_BRANCH" >/dev/null 2>&1 || {
  fail "nome de branch de destino invalido: $TARGET_BRANCH"
}

[[ -r /dev/tty && -w /dev/tty ]] || fail "e necessario executar o script em um terminal interativo"

if [[ -d .git/rebase-merge || -d .git/rebase-apply ]] || git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1; then
  fail "ha um merge ou rebase em andamento; finalize-o antes de publicar"
fi

# Preserve the original repository as `origin` and use a dedicated publication
# remote for the paper artifact.
if git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  publication_url="$(git remote get-url "$REMOTE_NAME")"
  case "$publication_url" in
    "$REPOSITORY_URL"|"$REPOSITORY_PAGE"|git@github.com:Sfgiovanni/BBQ---Bode.git)
      ;;
    *)
      fail "o remote $REMOTE_NAME aponta para '$publication_url', e nao para '$REPOSITORY_URL'"
      ;;
  esac
else
  git remote add "$REMOTE_NAME" "$REPOSITORY_URL"
fi

IFS= read -r -s -p "Token do GitHub (Contents: Read and write): " GITHUB_TOKEN </dev/tty
printf '\n' >/dev/tty
[[ -n "$GITHUB_TOKEN" ]] || fail "nenhum token foi informado"

umask 077
ASKPASS_FILE="$(mktemp "${TMPDIR:-/tmp}/bbq-bode-git-askpass.XXXXXX")"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'case "$1" in' \
  '  *Username*) printf "%s\\n" "x-access-token" ;;' \
  '  *Password*) printf "%s\\n" "$GITHUB_TOKEN" ;;' \
  '  *) printf "\\n" ;;' \
  'esac' >"$ASKPASS_FILE"
chmod 700 "$ASKPASS_FILE"

git_auth() {
  GITHUB_TOKEN="$GITHUB_TOKEN" \
  GIT_ASKPASS="$ASKPASS_FILE" \
  GIT_TERMINAL_PROMPT=0 \
    git "$@"
}

echo "Validando o repositorio de publicacao..."
git_auth ls-remote "$REMOTE_NAME" >/dev/null || {
  fail "nao foi possivel acessar $REPOSITORY_PAGE; confira o token e o repositorio"
}

remote_ref="$REMOTE_NAME/$TARGET_BRANCH"

fetch_target() {
  if ! git_auth ls-remote --exit-code --heads "$REMOTE_NAME" "$TARGET_BRANCH" >/dev/null 2>&1; then
    return 1
  fi
  git_auth fetch --prune "$REMOTE_NAME" \
    "+refs/heads/$TARGET_BRANCH:refs/remotes/$REMOTE_NAME/$TARGET_BRANCH"
}

remote_branch_exists=0
if fetch_target; then
  remote_branch_exists=1
  echo "Branch remota $TARGET_BRANCH encontrada e atualizada localmente."
else
  echo "O repositorio esta vazio; $TARGET_BRANCH sera criada no primeiro push."
fi

echo "Preparando os arquivos versionaveis..."
git add -A

# GitHub rejects blobs above 100 MiB. Stop before committing an object that
# could not be published.
oversized_file=""
while IFS= read -r -d '' path; do
  size="$(git cat-file -s ":$path" 2>/dev/null || printf '0')"
  if (( size > 100 * 1024 * 1024 )); then
    oversized_file="$path ($size bytes)"
    break
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z)
[[ -z "$oversized_file" ]] || fail "arquivo maior que 100 MiB no commit: $oversized_file"

if ! git diff --cached --quiet; then
  commit_message="${1:-$DEFAULT_MESSAGE}"
  [[ -n "$commit_message" ]] || commit_message="$DEFAULT_MESSAGE"
  git commit -m "$commit_message"
else
  echo "Nao ha alteracoes novas para criar commit; sincronizando os commits existentes."
fi

sync_with_remote() {
  (( remote_branch_exists == 1 )) || return 0

  if git merge-base --is-ancestor "$remote_ref" HEAD; then
    return 0
  fi

  git merge-base HEAD "$remote_ref" >/dev/null 2>&1 || {
    fail "os historicos local e remoto nao possuem ancestral comum; nenhum push foi feito"
  }

  echo "A branch remota avancou; reaplicando o commit local sobre ela..."
  if ! git rebase "$remote_ref"; then
    conflict_files="$(git diff --name-only --diff-filter=U | paste -sd ', ' -)"
    git rebase --abort >/dev/null 2>&1 || true
    fail "o rebase encontrou conflitos${conflict_files:+ em: $conflict_files}. O rebase foi abortado e nenhum force push foi feito"
  fi
}

sync_with_remote

# If another collaborator publishes between fetch and push, fetch once more,
# rebase safely, and retry. Force push is never used.
for attempt in 1 2; do
  before_push=""
  if (( remote_branch_exists == 1 )); then
    before_push="$(git rev-parse "$remote_ref")"
  fi

  echo "Enviando HEAD para $TARGET_BRANCH (tentativa $attempt/2)..."
  if git_auth push "$REMOTE_NAME" "HEAD:$TARGET_BRANCH"; then
    echo "Publicado com sucesso em $REPOSITORY_PAGE/tree/$TARGET_BRANCH"
    exit 0
  fi

  echo "O push foi recusado; verificando se a branch remota mudou..."
  if ! fetch_target; then
    fail "a branch continua ausente; verifique a permissao Contents: Read and write"
  fi

  remote_branch_exists=1
  after_push="$(git rev-parse "$remote_ref")"
  if [[ -n "$before_push" && "$before_push" == "$after_push" ]]; then
    fail "o remoto nao mudou; verifique a permissao do token ou a protecao da branch"
  fi
  sync_with_remote
done

fail "a branch remota mudou novamente durante o envio; execute o script outra vez"
