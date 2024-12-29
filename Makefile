

run-ui:
	streamlit run commands/ui/main.py

encrypt-configs:
	python commands/encrypt_configs.py

decrypt-configs:
	python commands/decrypt_configs.py

recreate-crypto-token:
	python commands/recreate_crypto_token.py

sync-infra:
	python commands/sync_infrastructure.py

sync-apps:
	python commands/public_app.py

sync-domains:
	python commands/prepare_domains.py

sync-registries:
	python commands/login_docker_registry.py

sync-envs:
	python commands/confirm_environments.py
