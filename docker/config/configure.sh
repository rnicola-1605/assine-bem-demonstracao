#!/bin/bash
# sed -e 's/[@]/\\@/g'
# sed -e 's/[]\/$*.^[]/\\&/g'

# Gera novo arquivo do zope.conf a partir do .empty
cp ${INSTANCE_PATH}/etc/zope.conf.empty ${INSTANCE_PATH}/etc/zope.conf
