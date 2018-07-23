publish:
	python3 gen.py
	cp CNAME dist
	cd dist && git init && git config user.name 'opskumu' && git config user.email 'opskumu@gmail.com' && git add . && git commit -m 'Auto publisher' && git push --force --quiet "git@github.com:opskumu/opskumu.com.git" master:gh-pages > /dev/null 2>&1
	rm -rf dist 
