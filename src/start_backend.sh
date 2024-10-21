# Starting multiple processes in a single command, allowing one CTRL-C to kill them all
# Taken from https://stackoverflow.com/questions/3004811/how-do-you-run-multiple-programs-in-parallel-from-a-bash-script
(trap 'kill 0' SIGINT;   ai_chains &  llm_wrapper &  ai_brain   )