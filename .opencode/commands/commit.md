---
description: Propone un mensaje de commit siguiendo Conventional Commits
---
Revisa los cambios en stage y propón UN mensaje de commit.

Reglas:
- Formato: tipo(alcance): resumen en imperativo, máximo 72 caracteres
- Tipos válidos: feat, fix, docs, refactor, test, chore
- Si los cambios mezclan temas distintos, dime cómo dividirlos en varios commits
- NO ejecutes el commit, solo propón el mensaje

Cambios en stage:
!`git diff --staged`
