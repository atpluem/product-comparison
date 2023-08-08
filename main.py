import pandas as pd
import argparse
from bs4 import BeautifulSoup

# Extract column names
def extract_column_from_header(row):
    if row.br: row.br.extract()
    if row.a: row.a.extract()
    if row.sup: row.sup.extract()

    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name 

def main() -> None:
    website_paths = ['src/website1.html', 
                     'src/website2.html',
                     'src/website3.html']

    for i_web, path in enumerate(website_paths):
        with open(path, 'r') as f:
            html_data = f.read()
        soup = BeautifulSoup(html_data, 'lxml')
        html_table = soup.find_all('table')[0]

        # Extract column names
        if i_web == 0:
            column_names = []
            for row in html_table.find_all('th'):
                name = extract_column_from_header(row)
                if name is not None and len(name) > 0:
                    column_names.append(name)
        
        product_dict = dict.fromkeys(column_names)
        # Set dict value to empty list
        for key in product_dict.keys():
            product_dict[key] = []  

        for rows in html_table.find_all('tr'):
            # skip table heading
            if rows.th: continue
            row = rows.find_all('td')
            for i, col_name in enumerate(column_names):
                product_dict[col_name].append(row[i].contents[0])
        
        if i_web == 0:
            result = pd.DataFrame(product_dict)
            result['CarPrice'] = result['CarPrice'].astype('int')
            result.rename(columns={"CarPrice": "CarPrice_{0}".format(i_web+1)}, 
                        inplace=True)
        else:
            temp = pd.DataFrame(product_dict)
            temp['CarPrice'] = temp['CarPrice'].astype('int')
            temp.rename(columns={"CarPrice": "CarPrice_{0}".format(i_web+1)}, 
                        inplace=True)
            result = pd.merge(result, temp, how='inner', on=['SKU', 'SupplierName'])
    
    # passing argument to filter SKU
    parser = argparse.ArgumentParser(description='Process arguments')
    parser.add_argument('--sku', type=str, help='SKU argument')
    args = parser.parse_args()

    # filter SKU
    result = result[result['SKU'].str.contains('{0}'.format(args.sku))]
    result.to_csv('src/result.csv', index=False)

if __name__ == "__main__":
    main()