#!/bin/bash

# Usage:
#   source custom_env.sh [venv-name] [project-name]
#   source custom_env.sh --venv <venv-name>
#   source custom_env.sh --project <project-name>
#
# Cases:
#   - No args: venv=venv, project=config
#   - One arg: defaults to project name
#   - --venv only: venv=<venv-name>, project=config
#   - --project only: venv=venv, project=<project-name>
#   - Two args: venv=<arg1>, project=<arg2>

# Defaults
venv_name="venv"
django_project="config"

# Parse arguments
if [ $# -eq 0 ]; then
    echo "⚠️ No arguments provided. Defaulting venv='$venv_name', project='$django_project'"
elif [ $# -eq 1 ]; then
    # Assume single argument is project name
    django_project=$1
    echo "⚠️ No venv name provided. Defaulting venv='$venv_name'"
    echo "✅ Using project name='$django_project'"
elif [ $# -eq 2 ]; then
    # Two positional arguments: venv + project
    venv_name=$1
    django_project=$2
    echo "✅ Using venv='$venv_name', project='$django_project'"
else
    # Handle flags
    while [[ $# -gt 0 ]]; do
        case $1 in
            --venv)
                venv_name=$2
                shift 2
                ;;
            --project)
                django_project=$2
                shift 2
                ;;
            *)
                echo "❌ Unknown option: $1"
                exit 1
                ;;
        esac
    done
    echo "✅ Using venv='$venv_name', project='$django_project'"
fi

# Create the venv
python -m venv "$venv_name"

# Cross-platform venv Activation
if [ -f "$venv_name/Scripts/activate" ]; then
    # Windows (Git Bash / cmd)
    source "$venv_name/Scripts/activate"
elif [ -f "$venv_name/bin/activate" ]; then
    # Linux/macOS
    source "$venv_name/bin/activate"
else
    echo "❌ Could not find activate script for venv '$venv_name'"
    exit 1
fi

# Define installfreeze function
installfreeze() {
    pip install "$@"
    pip freeze > requirements.txt
    echo "✅ Installed: $@ and updated requirements.txt"
}

echo "✅ Virtual environment '$venv_name' created and activated."

# install django and rest framework libs
installfreeze django djangorestframework

# Start Django project with given name
django-admin startproject "$django_project" .
echo "✅ Django project '$django_project' created in current directory."

# Instructions
echo "➡️  Use: installfreeze <packages> to install and freeze in one line."
