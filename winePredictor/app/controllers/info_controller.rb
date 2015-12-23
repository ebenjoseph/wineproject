class InfoController < ApplicationController

	def index
	end

	def info
	end

	def post_info
		puts "TEST"
		puts params[:text_val]

		File.write(Rails.root.join('mallet', 'data', 'inputfile.txt'), params[:text_val])
		flag = system("cat ./mallet/data/inputfile.txt | python ./mallet/ngram_format.py > ./mallet/data/inputfile2.txt")
		puts flag
		system("./mallet/bin/mallet classify-file --input ./mallet/data/inputfile2.txt --output ./mallet/tempoutput.txt --classifier ./mallet/wine_5k.classifier.trial0")
		system("cat ./mallet/tempoutput.txt | python ./mallet/outputsorter.py > ./mallet/data/outputfile.txt")

		redirect_to(:controller => 'info', :action => 'info')
	end
end