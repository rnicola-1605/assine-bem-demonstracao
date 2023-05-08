#!/bin/bash
# sed -e 's/[@]/\\@/g'
# sed -e 's/[]\/$*.^[]/\\&/g'

# Gera novo arquivo do zope.conf a partir do .empty
cp ${INSTANCE_PATH}/etc/zope.conf.empty ${INSTANCE_PATH}/etc/zope.conf

URL_DB=$(cat /run/secrets/zope_secrets | grep -oP '(?<=\bURL_DB=)[^;]+' | sed -e 's/[@]/\\@/g')
sed -i "s@\${URL_DB}@${URL_DB}@" ${INSTANCE_PATH}/etc/zope.conf

ENCODING_DB=$(cat /run/secrets/zope_secrets | grep -oP '(?<=\bENCODING_DB=)[^;]+' | sed -e 's/[@]/\\@/g')
sed -i "s@\${ENCODING_DB}@${ENCODING_DB}@" ${INSTANCE_PATH}/etc/zope.conf
