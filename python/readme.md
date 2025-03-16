# Google Cloud Run에 gRPC 서비스 배포하기

이 문서는 Google Cloud Run에 gRPC 서비스를 배포하는 방법을 설명합니다.

## Environment Variable Settings

```
PROJECT_ID=<YOUR_PROJECT_ID>
ORGANIZATION_ID=<YOUR_ORGANIZATION_ID>
LOCATION=<YOUR_LOCATION>
SERVICE_ACCOUNT_NAME=<YOUR_SERVICE_ACCOUNT_NAME>
SERVICE_ACCOUNT_EMAIL="$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com"
CLOUDRUN_SERVICE=<YOUR_CLOUDRUN_SERVICE>
ARTIFACT_REGISTRY_REPO=<YOUR_ARTIFACT_REGISTRY_REPO>
IMAGE_NAME=<YOUR_IMAGE_NAME>
IMAGE_TAG="v1"
```

## 1. 프로젝트 설정

1.  Google Cloud 프로젝트를 선택하거나 생성합니다.
2.  Cloud Run API를 활성화합니다.
3.  `gcloud`를 사용하여 Google Cloud에 로그인하고 프로젝트를 설정합니다.

    ```bash
    gcloud auth login
    gcloud config set project $PROJECT_ID
    ```

### API Setup

```
gcloud services enable run.googleapis.com --project=$PROJECT_ID
```

### Create Artifact Registry Repository

```
gcloud artifacts repositories create "$ARTIFACT_REGISTRY_REPO" \
    --repository-format=docker \
    --location="$LOCATION" \
    --description="Docker repository for $CLOUDRUN_SERVICE" \
    --project="$PROJECT_ID"
```


## Service Account

### Create SA

```
gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
  --description="Service account for gRPC sample Cloud Run service" \
  --display-name="$SERVICE_ACCOUNT_NAME" \
  --project="$PROJECT_ID"
```


### Permission Configuration

-   Grant Logging Admin role (for Cloud Run log writing)

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
  --role="roles/logging.admin"
```

-   Grant Cloud Service Account User role (necessary for Cloud Run to use the service account)

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/run.invoker"
```

- Grant the roles/run.invoker role to the Cloud Run service account

```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_EMAIL" \
    --role="roles/iam.serviceAccountUser"
```


## Create Cloud Run Service

```
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

## 2. Docker 이미지 생성


- `.proto` 파일을 컴파일하여 Python 코드를 생성합니다.

    ```bash
    python -m grpc_tools.protoc -I./protos --python_out=./server --grpc_python_out=./server ./protos/calculator.proto
    python -m grpc_tools.protoc -I./protos --python_out=./client --grpc_python_out=./client ./protos/calculator.proto
    ```

- Docker 이미지를 빌드하고 Google Container Registry (GCR)에 푸시합니다.

    ```bash
    docker build -t "$LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO/$IMAGE_NAME:$IMAGE_TAG" ./server
    ```

- For debugging
docker build --no-cache --progress=plain -t "$LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO/$IMAGE_NAME:$IMAGE_TAG" ./server 2>&1 | tee build.log


- Configure Docker
Run the following command to configure gcloud as the credential helper for the Artifact Registry domain associated with this repository's location:

```
gcloud auth configure-docker $LOCATION-docker.pkg.dev
```

- Push the docker image
```
docker push "$LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO/$IMAGE_NAME:$IMAGE_TAG"
```

### Deploy Cloud Run Service

```
gcloud run deploy "$CLOUDRUN_SERVICE" \
  --image="$LOCATION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REGISTRY_REPO/$IMAGE_NAME:$IMAGE_TAG" \
  --region="$LOCATION" \
  --max-instances=1 \
  --concurrency=1 \
  --allow-unauthenticated \
  --set-env-vars="PROJECT_ID=$PROJECT_ID,REGION=$LOCATION" \
  --service-account="$SERVICE_ACCOUNT_EMAIL" \
  --project="$PROJECT_ID" \
  --port=8080 \
  --use-http2
```

### Get Cloud Run Service URL and Service Account Email

```
CLOUDRUN_SERVICE_URL=$(gcloud run services describe "$CLOUDRUN_SERVICE" --region="$LOCATION" --format="value(status.url)" --project="$PROJECT_ID")
```


### Client testing

```
python client.py <server_address> <operation> <a> <b> [-k]
```

- <server_address>: gRPC 서버의 주소입니다. 예를 들어, localhost:50051 또는 127.0.0.1:50051과 같이 입력합니다.
- <operation>: 수행할 연산입니다. add 또는 subtract를 입력합니다.
- <a>: 첫 번째 피연산자입니다. 실수 값을 입력합니다.
- <b>: 두 번째 피연산자입니다. 실수 값을 입력합니다.
- [-k]: 플레인 텍스트 연결을 사용하려면 -k 또는 --plaintext 옵션을 추가합니다. 이 옵션을 사용하면 보안 연결이 아닌 일반 연결을 사용합니다. 로컬 테스트나 디버깅 시 유용합니다.

다음은 몇 가지 예시입니다.

- 덧셈 연산:
```Bash
python client.py localhost:50051 add 10.5 5.2
```

- 뺄셈 연산:
```Bash
python client.py localhost:50051 subtract 20 8
```

- 플레인 텍스트 연결 사용:
```Bash
python client.py localhost:50051 add 5 3 -k
```

## 주의사항

* Cloud Run은 서버리스 플랫폼이므로 사용량에 따라 비용이 발생합니다.
* gRPC 서비스는 HTTP/2 프로토콜을 사용하므로 클라이언트도 HTTP/2를 지원해야 합니다.
* Cloud Run은 8080 포트만 지원합니다. Dockerfile의 EXPOSE와 gcloud run deploy의 port를 8080으로 맞추어야 합니다.
* 만약, 클라이언트와 서버가 통신이 안된다면, cloud run 서비스의 로그를 확인하십시오.
* 만약, 로컬에서 docker build를 할 수 없다면, cloud build를 이용하여 docker image를 빌드하고 push 하는 것을 추천합니다.