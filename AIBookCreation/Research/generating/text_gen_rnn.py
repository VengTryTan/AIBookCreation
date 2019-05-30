from textgenrnn import textgenrnn

textgen = textgenrnn()

# textgen.generate(interactive=True, top_n=5)
textgen.train_from_file('data/book.txt', num_epochs=1)
textgen.generate_samples()
