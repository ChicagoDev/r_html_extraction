import sys
from utils.rds_to_pandas_df import parse_one_rds_file_to_html_extracted_pandas_df as convert_rds

(script, rds_filename, out_filename) = sys.argv

df = convert_rds(rds_filename)

#df.to_csv(out_filename, sep='\t', doublequote=True, header=True)

df.to_csv(out_filename, sep='\t', doublequote=True, header=False)

