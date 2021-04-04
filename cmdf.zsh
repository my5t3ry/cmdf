command_not_found_handler() {
  result="$(curl -X POST -s --data-urlencode "cmd=$*" http://127.0.0.1:7755/correct | python3 -c "import sys, json; print(json.load(sys.stdin)['cmd'])")"
  echo -n "execute $result (y/n)? "
  read answer
  if [ "$answer" != "${answer#[Yy]}" ]; then
    echo "exec $result"
    ($result)
    return 0
  else
    return $?
  fi
}
