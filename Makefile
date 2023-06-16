all:
	docker-compose up -d

clean:
	docker-compose down --rmi all

.PHONY: all clean
