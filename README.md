# XML-to-CSV-file-conversion-
Converting XML file into a separate CSV format as per the requirement 
First Script (xml_to_csv):Parses the XML file using xml.etree.ElementTree.Extracts necessary data elements and stores them in a list of lists.Converts the list to a Pandas DataFrame and writes it to a CSV file with columns matching the sample output.Second Script (split_csv_by_measinfoid):Reads the CSV file generated by the first script.Identifies unique MeasinfoID values.Splits the DataFrame based on MeasinfoID and saves each subset as a separate CSV file in the specified output directory.
