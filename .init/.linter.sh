#!/bin/bash
cd /home/kavia/workspace/code-generation/task-management-system-7109-7126/todo_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

