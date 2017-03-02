maprcli stream delete -path /bell-project
maprcli stream create -path /bell-project
maprcli stream edit -path /bell-project -produceperm p -consumeperm p -copyperm p -topicperm p
maprcli stream topic create -path /bell-project -topic notify
maprcli stream topic create -path /bell-project -topic bellNotify
