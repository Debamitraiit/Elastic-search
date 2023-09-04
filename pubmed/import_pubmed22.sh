#!/bin/bash
curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

for eachjson in /home/ubuntu/pubmed/json/*.json.bz2
	do
		bzcat ${eachjson} | python preprocess22.py ${eachjson} 1> ${eachjson}_bulk.json
		echo >> ${eachjson}_bulk.json
		curl -XPOST http://localhost:9200/_bulk?pretty -H "Content-type: application/x-ndjson" --data-binary @${eachjson}_bulk.json 1
		rm ${eachjson}_bulk.json
	done

