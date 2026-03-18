# #!/usr/bin/env bash
# # Obsidian vaultから進捗.mdを取得してreference/progress/に配置する
# set -euo pipefail

# OBSIDIAN_REPO="junya737/obsidian-personal"
# FILE_PATH="Kaggle/deep-past-2026/進捗.md"
# DEST="reference/progress/進捗.md"

# gh api "repos/${OBSIDIAN_REPO}/contents/${FILE_PATH}" \
#   --jq '.content' | base64 -d > "${DEST}"

# echo "Synced: ${DEST}"
