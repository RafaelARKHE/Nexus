#!/bin/bash
# Nexus — sincronização automática com o GitHub (rede de segurança)
# Chamado pelos hooks SessionStart e SessionEnd do Claude Code.
# Commita mudanças pendentes com timestamp, faz pull --rebase e push da main.
# Nunca resolve conflitos: em caso de conflito, aborta o rebase e registra no log.

NEXUS="/Users/rafaelarche/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus"
LOG="$NEXUS/.claude/hooks/sync.log"

log() {
  echo "[$(date '+%d/%m/%Y %H:%M:%S')] $1" >> "$LOG"
}

cd "$NEXUS" || { log "ERRO: não encontrou a raiz do Nexus"; exit 0; }

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -z "$BRANCH" ]; then
  log "ERRO: não é um repositório git"
  exit 0
fi

# Rebase interrompido de uma execução anterior? Não mexer.
if [ -d "$(git rev-parse --git-dir)/rebase-merge" ] || [ -d "$(git rev-parse --git-dir)/rebase-apply" ]; then
  log "AVISO: rebase em andamento — sincronização pulada, resolver manualmente"
  exit 0
fi

CHANGES=$(git status --porcelain)
AHEAD=$(git log "origin/$BRANCH..$BRANCH" --oneline 2>/dev/null | wc -l | tr -d ' ')

if [ -z "$CHANGES" ] && [ "$AHEAD" = "0" ]; then
  # Nada local para enviar — ainda assim puxar novidades do remoto (sessões web, outros dispositivos)
  git fetch origin "$BRANCH" --quiet 2>>"$LOG"
  BEHIND=$(git log "$BRANCH..origin/$BRANCH" --oneline 2>/dev/null | wc -l | tr -d ' ')
  if [ "$BEHIND" != "0" ]; then
    if git pull --rebase origin "$BRANCH" --quiet 2>>"$LOG"; then
      log "OK: $BEHIND commit(s) recebidos de origin/$BRANCH (nada local para enviar)"
    else
      git rebase --abort 2>/dev/null
      log "CONFLITO: pull de origin/$BRANCH falhou — rebase abortado, resolver manualmente"
    fi
  fi
  exit 0
fi

if [ -n "$CHANGES" ]; then
  git add -A 2>>"$LOG"
  git commit -m "sync: alterações pendentes de $(date '+%d/%m/%Y %H:%M')" --quiet 2>>"$LOG"
  log "COMMIT: rede de segurança capturou mudanças não commitadas"
fi

if ! git pull --rebase origin "$BRANCH" --quiet 2>>"$LOG"; then
  git rebase --abort 2>/dev/null
  log "CONFLITO: pull --rebase de origin/$BRANCH falhou — rebase abortado, push não realizado"
  exit 0
fi

if git push origin "$BRANCH" --quiet 2>>"$LOG"; then
  log "OK: $BRANCH sincronizada com o GitHub"
else
  log "ERRO: push para origin/$BRANCH falhou (sem rede?) — commits locais preservados"
fi

exit 0
