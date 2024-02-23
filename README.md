# WES LLM Server

This repo contains a Kubernetes deployment of the llama.cpp server.

In order to deploy the server, you need to:

First, ensure the `/media/plugin-data/llama-cpp-models` directory exists. This will be where models will be stored.

Next, we need to add a model. In my case, I rsyned one I downloaded from LM Studio's cache:
```
rsync -av /Users/sean/.cache/lm-studio/models/TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf /media/plugin-data/llama-cpp-models/TheBloke/phi-2-GGUF/phi-2.Q4_K_S.gguf
```

Next, clone and enter this repo:

```
git clone https://github.com/waggle-sensor/wes-llm-server
cd wes-llm-server
```

Make sure the `--model` flag in the `deployment.yaml` points to your model.

Finally, you can deploy the whole thing with:

```sh
kubectl apply -k .
```
