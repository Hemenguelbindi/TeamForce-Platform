'''
	usage: import pdf
		   ...
		   d = pdf.getInfo('sample.pdf')
'''

import io
import re

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)

def extract_text_from_pdf(pdf_path):
	resource_manager = PDFResourceManager()
	fake_file_handle = io.StringIO()
	converter = TextConverter(resource_manager, fake_file_handle)
	page_interpreter = PDFPageInterpreter(resource_manager, converter)

	with open(pdf_path, 'rb') as fh:
		for page in PDFPage.get_pages(fh,
									  caching=True,
									  check_extractable=True):
			page_interpreter.process_page(page)

		text = fake_file_handle.getvalue()

	# close open handles
	converter.close()
	fake_file_handle.close()

	if text:
		return text


def getInfo(path_to_pdf):

	'''

	:param: path_to_pdf
	:return: dict = { name1, name2, name3, phone, email}

	'''

	d_name = {}

	# parse pdf
	text = extract_text_from_pdf(path_to_pdf)

	# get names
	emb = NewsEmbedding()
	segmenter = Segmenter()
	morph_vocab = MorphVocab()
	ner_tagger = NewsNERTagger(emb)
	names_extractor = NamesExtractor(morph_vocab)
	doc = Doc(text)
	doc.segment(segmenter)
	doc.tag_ner(ner_tagger)
	for span in doc.spans:
		span.normalize(morph_vocab)
	for span in doc.spans:
		if span.type == PER:
			span.extract_fact(names_extractor)
	names = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}

	if len(names) > 0:
		l = next(iter(names)).split()
		if len(l) >= 1:
			d_name['name1'] = next(iter(names)).split()[0]
			if len(l) >= 2:
				d_name['name2'] = next(iter(names)).split()[1]
				if len(l) >= 3:
					d_name['name3'] = next(iter(names)).split()[2]

	# get mail
	sp = text.split()
	for c in sp:
		if '@' in c:
			# print(c)
			d_name['mail'] = c

	# get phone
	ph = ''.join(re.findall(r'(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})', text)[0])
	d_name['phone'] = ph

	return d_name
