#!/bin/bash

#echo $1
case $1 in
	-j|-J)
		echo "JAVA" > readyToSubmit.txt
		echo "Language: Java"
		;;
	-cpp|-CPP)
		echo "C++" > readyToSubmit.txt
		echo "Language: C++"
		;;
	-cs|-CS)
		echo "C#" > readyToSubmit.txt
		echo "Language: C#"
		;;
	-p|-P)
		echo "PYTHON" > readyToSubmit.txt
		echo "Language: Python"
		;;
	*)
		input="bad"
		# echo $input
		while [[ $input == "bad" ]]; do
			echo "Please input your programming language ( j for Java, cpp for C++, cs for C#, or p for Python ):"
			read language
			case $language in
				j|J)
					echo "JAVA" > readyToSubmit.txt
					echo "Language: Java"
					input="good enough"
					;;
				cpp|CPP)
					echo "C++" > readyToSubmit.txt
					echo "Language: C++"
					input="good enough"
					;;
				cs|CS)
					echo "C#" > readyToSubmit.txt
					echo "Language: C#"
					input="good enough"
					;;
				p|P)
					echo "PYTHON" > readyToSubmit.txt
					echo "Language: Python"
					input="good enough"
					;;
				*)
					echo "Your input was invalid. Please try again."
					;;
			esac
		done
		;;
esac

input="bad"
while [[ $input == "bad" ]]; do
	echo "Please input your auburn username: "
	read auName
	echo "Is $auName correct? (y/n)"
	read answer
	if [[ "$answer" =~ [Yy][eE]?[sS]? ]]; then 
		echo $auName >> readyToSubmit.txt
		input="good enough"
	fi
done

echo "Your code has been finalized! Your submission will be eligible for grading when you push to Master."
echo "If you ran this script on accident, simply delete readyToSubmit.txt"
