#!/bin/bash
cd /home/kavia/workspace/code-generation/flowcode-visual-executor-48294-49002/js_code_executor_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

