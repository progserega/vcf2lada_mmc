#!/bin/bash
in_file="${1}"
out_file="${2}"

cat /dev/null > "${out_file}"

cat "${in_file}"|while read text
do
	text="`echo $text|sed 's/^FN/ContactName/'`"
	if [ ! -z "`echo $text|grep TEL`" ]
	then
		text="`echo $text|tr ' -)(' '-'|sed 's/-//g'`"
	fi
	echo $text |iconv -f utf8 -t cp1251 >> "${out_file}"
done
