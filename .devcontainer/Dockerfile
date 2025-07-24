FROM python:3.13.5-bookworm as builder

COPY app/requirements.txt .

RUN set -ex \
&& apt-get update -yqq \
&& ACCEPT_EULA=Y apt-get install --no-install-recommends -yqq git net-tools iputils-ping mc
RUN pip3 install -r requirements.txt
# Добавляем GPG-ключ Temurin
RUN wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public > /tmp/key.asc && \
    gpg --dearmor -o /etc/apt/trusted.gpg.d/adoptium.gpg /tmp/key.asc && \
    rm /tmp/key.asc


# # Добавляем репозиторий Temurin для Debian Bookworm
# RUN echo "deb https://packages.adoptium.net/artifactory/deb bookworm main" | tee /etc/apt/sources.list.d/adoptium.list

# # Устанавливаем OpenJDK 21 из Temurin
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends temurin-21-jdk

# # Опционально: задаем переменные окружения (путь может отличаться)
# ENV JAVA_HOME=/usr/lib/jvm/temurin-21-jdk-amd64
# ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV JDK_VERSION=21.0.7+6
# Для сборки под обычный Linix x64
# ENV JDK_BUILD=openjdk21u-jdk_x64_linux_hotspot_21.0.7_6.tar.gz
# Для сборки под MacOS
ENV JDK_BUILD=openjdk21u-jdk_aarch64_linux_hotspot_21.0.7_6.tar.gz
ENV JDK_URL=https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.7%2B6/${JDK_BUILD}

RUN mkdir -p /opt/java && \
    wget -q ${JDK_URL} -O /tmp/${JDK_BUILD} && \
    tar -xzf /tmp/${JDK_BUILD} -C /opt/java && \
    rm /tmp/${JDK_BUILD}

# Устанавливаем JAVA_HOME и обновляем PATH
ENV JAVA_HOME=/opt/java/jdk-21.0.7+6
ENV PATH="${JAVA_HOME}/bin:${PATH}"