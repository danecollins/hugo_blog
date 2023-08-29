#!/bin/bash

rsync -avm --exclude '.git' --exclude '.DS_Store' --exclude 'recipe' public/ ../danecollins.github.io

