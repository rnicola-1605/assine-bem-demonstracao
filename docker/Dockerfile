FROM python:3.7

LABEL MAINTAINER="Rodrigo Nicola"
LABEL AUTHOR="Rodrigo Nicola"
LABEL AUTHOR_EMAIL="rnicolasilva@gmail.com"

ARG uid=1000
ARG user=zope
ARG path=/zope/
ARG userZope
ARG passZope
ARG portZope

RUN if [ -z $userZope ]; then echo 'userZope nao foi informado. Cancelando.' && exit 1; echo 'OK'; fi;
RUN if [ -z $passZope ]; then echo 'passZope nao foi informado. Cancelando.' && exit 1; echo 'OK'; fi;
RUN if [ -z $portZope ]; then echo 'portZope nao foi informado. Cancelando.' && exit 1; echo 'OK'; fi;


# # -- LANG do container deve ser em UTF-8
ENV LANG=en_us.UTF-8

ENV DIRPATH=$path
ENV userZope=$userZope
ENV passZope=$passZope
ENV portZope=$portZope

RUN apt update

RUN useradd -ms /bin/bash $user

RUN mkdir $path
RUN chown -R $user:$user "$path"

USER $user

RUN python3 -m venv $path
RUN echo 'export LANG="en_us.UTF-8"' >> $path/bin/activate

WORKDIR $path/

ADD --chown=zope ./config ./config
ADD --chown=zope ./Start_products ./Start_products
ADD --chown=zope ./requirements.txt ./requirements.txt

# Instala o Zope e outros produtos
RUN bin/pip install --upgrade pip && \
    bin/pip install --upgrade \
        -r https://zopefoundation.github.io/Zope/releases/5.5/requirements-full.txt \
        -r requirements.txt \
        git+https://github.com/rnicola-1605/assine-bem-demonstracao

RUN ./bin/mkwsgiinstance --dir instance --user ${userZope}:${passZope}

ENV INSTANCE_PATH=${DIRPATH}/instance

RUN cp config/* ${INSTANCE_PATH}/etc/.

# # -- Altera as instancias conforme INSTANCE_PATH do ARG.
RUN sed -i --expression "s@INSTANCIA@$INSTANCE_PATH@" ${INSTANCE_PATH}/etc/zope.conf.empty
RUN sed -i --expression "s@INSTANCIA@$INSTANCE_PATH@" ${INSTANCE_PATH}/etc/zope.ini

# adiciona e altera o zopectl
ADD --chown=zope ./commands/zopectl ${path}/
RUN chmod +x ${path}/zopectl
RUN sed -i --expression "s@INSTANCIA@$path@" ${path}/zopectl
RUN sed -i --expression "s@PATHINS@$INSTANCE_PATH@" ${path}/zopectl
RUN sed -i --expression "s@USERINS@$user@" ${path}/zopectl

# starta os produtos da assine bem
RUN cp -R Start_products/ ${path}/lib/python3.7/site-packages/Products

# Ajuste o zope.conf e o zope.ini
RUN sed -i '/port = 8080/d' ${INSTANCE_PATH}/etc/zope.ini
RUN sed -i "s/host = 127.0.0.1/listen = *:$portZope/" ${INSTANCE_PATH}/etc/zope.ini
RUN echo "datetime-format international" >> ${INSTANCE_PATH}/etc/zope.conf
RUN ln -s ${INSTANCE_PATH}/var/log/event.log


# # -- Publica o container na porta
EXPOSE $portZope

# # -- Comando executado toda vez que o container eh iniciado.
# # -- Roda script de configuracao que gera zope.conf a partir das secrets.
# # -- Inicia zope e ativa virtualenv
# ${DIRPATH}/bin/python ${DIRPATH}/config/configure.py && \

CMD sh ${INSTANCE_PATH}/etc/configure.sh && \
    ${DIRPATH}/bin/runwsgi -v instance/etc/zope.ini && \
    source ${DIRPATH}/bin/activate
