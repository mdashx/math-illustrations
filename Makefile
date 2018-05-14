ex10:
	cat page-setup.ps vector-procedures.ps drawing-procedures.ps chp1-ex1-10.ps > tmp.ps
	ps2pdf tmp.ps tmp.pdf

svg:
	epstopdf $(file).eps --outfile tmp.pdf
	pdf2svg tmp.pdf $(file).svg


