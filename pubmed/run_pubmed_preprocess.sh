
for i in /home/ubuntu/pubmed/pubmed23n*.gz
do
	python3 pubmedxmltojson3.py ${i} 1> ${i%.xml.gz}.json 2> ${i%.xml.gz}.log; bzip2 ${i%.xml.gz}.json
done

