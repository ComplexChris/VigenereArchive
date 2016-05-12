# VigenereArchive

Poly-alphabetic asymmetrical archive system. 

This programs utilizes a poly-alphabetic cipher (Vigenere encryption), zipfiles, and String IO instances to secure small volumes of text files and other bits of data such as rich text documents and files (.XML, .TXT, .RTF, .JPG, .MP4, .M4A, .WAV, .PDF, .MP3, etc)

With the simple UI, you can create, and start an archive in less than a minute! Then once aquainted, the program can start your decrypted archive in a temporary directory using the GUI to allow a simpler, intuitive file transfer system utilizing the native systems file explorer GUI! 

Given encryption type and version, use caution when importing files larger than ~50 MB, give or take depending on your system specs because the crypto-system literally has to process every char with a minimum of 1/4 of the data using block encryption implementation with data exceding a specific length (~2**15) 
