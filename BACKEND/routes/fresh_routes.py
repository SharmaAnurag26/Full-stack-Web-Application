from flask import Blueprint, jsonify
from database import connect_db
import pandas as pd

fresh_blueprint = Blueprint('fresh_api', __name__)



# Routing for the API for Fresh Enquiry data for Home page

@fresh_blueprint.route('/dealers', methods=['GET'])
def get_unique_dealers():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM (
                    SELECT `Dealer code` FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'
                    UNION
                    SELECT `Dealer code` FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'
                ) AS combined_dealers;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers": int(df.iloc[0, 0])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/sales', methods=['GET'])
def get_total_sales():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM (
                    SELECT `Customer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry status` = 'Closed' 
                      AND `Customer code` IS NOT NULL
                      AND `Enquiry Division` = 'Fresh Enquiry'

                    UNION ALL

                    SELECT `Customer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry status` = 'Closed' 
                      AND `Customer code` IS NOT NULL
                      AND `Enquiry Division` = 'Fresh Enquiry'
                ) AS all_sales;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@fresh_blueprint.route('/open-enquiries', methods=['GET'])
def get_open_enquiries():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM (
                    SELECT `Dealer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry status` = 'Pending' 
                      AND `Enquiry Division` = 'Fresh Enquiry'

                    UNION ALL

                    SELECT `Dealer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry status` = 'Pending' 
                      AND `Enquiry Division` = 'Fresh Enquiry'
                ) AS all_open_enquiries;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/total-fresh-enquiries', methods=['GET'])
def get_total_fresh_enquiries():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_fresh_enquiries
                FROM (
                    SELECT `Dealer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'

                    UNION ALL

                    SELECT `Dealer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'
                ) AS all_fresh_enquiries;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No fresh enquiries found"}), 404

        return jsonify({"total_fresh_enquiries": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@fresh_blueprint.route('/enquiry-types/fresh', methods=['GET'])
def get_fresh_enquiry_type_counts():
    try:
        with connect_db() as conn:
            query = """
                SELECT `Enquiry type`, COUNT(*) AS total
                FROM (
                    SELECT `Enquiry type` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'

                    UNION ALL

                    SELECT `Enquiry type` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'
                ) AS combined_types
                GROUP BY `Enquiry type`
                ORDER BY total DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry type data found"}), 404

        return jsonify({"fresh_enquiry_types": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@fresh_blueprint.route('/enquiry-sources/fresh', methods=['GET'])
def get_fresh_enquiry_sources():
    try:
        with connect_db() as conn:
            query = """
                SELECT `Source`, COUNT(*) AS total
                FROM (
                    SELECT `Source` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'

                    UNION ALL

                    SELECT `Source` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Fresh Enquiry'
                ) AS combined_sources
                GROUP BY `Source`
                ORDER BY total DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No source data found for fresh enquiries"}), 404

        return jsonify({"fresh_enquiry_sources": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Fresh Enquiry data for India  page
@fresh_blueprint.route('/unique-dealers/State/fresh', methods=['GET'])
def get_unique_dealers_per_state():
    try:
        with connect_db() as conn:
            query = """
                SELECT State, COUNT(*) AS UniqueDealers
                FROM (
                    SELECT `Dealer code`, MIN(State) AS State
                    FROM enquiryreportindiacsv
                    WHERE `Enquiry Division` = 'Fresh enquiry'
                    GROUP BY `Dealer code`
                ) AS unique_dealers
                GROUP BY State
                ORDER BY UniqueDealers DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No dealer data found for fresh enquiries"}), 404

        return jsonify({"fresh_enquiry_unique_dealers": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/product-sales/state-wise/India', methods=['GET'])
def get_product_sales_state_wise():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `State`, 
                    `Products interested`, 
                    COUNT(*) AS `Total Sales`
                FROM 
                    enquiryreportindiacsv
                GROUP BY 
                    `State`, 
                    `Products interested`
                ORDER BY 
                    `State`, 
                    `Total Sales` DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"state_wise_product_sales": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fresh_blueprint.route('/enquiry-types/state-wise/India', methods=['GET'])
def get_enquiry_types_state_wise():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `State` AS state,
                    `Products interested` AS product_name,
                    `Enquiry type` AS enquiry_type,
                    COUNT(*) AS enquiry_count
                FROM 
                    enquiryreportindiacsv
                WHERE
                    `Enquiry division` = 'Fresh Enquiry'
                GROUP BY 
                    `State`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `State`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"state_wise_enquiry_types": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fresh_blueprint.route('/enquiry-types/state-wise/India/converted', methods=['GET'])
def get_enquiry_types_converted():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `State` AS state,
                    `Products interested` AS product_name,
                    `Enquiry type` AS enquiry_type,
                    COUNT(*) AS enquiry_count
                FROM 
                    enquiryreportindiacsv
                WHERE
                    `Enquiry division` = 'Fresh enquiry'
                    AND `Enquiry status` = 'Closed'
                GROUP BY 
                    `State`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `State`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"converted_enquiry_types": df.to_dict(orient='records')}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/Idealers', methods=['GET'])
def get_unique_dealers_india():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM enquiryreportindiacsv 
                WHERE `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers_india": int(df.iloc[0, 0])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/Isales', methods=['GET'])
def get_total_sales_india():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM enquiryreportindiacsv 
                WHERE `Enquiry status` = 'Closed' 
                  AND `Customer code` IS NOT NULL
                  AND `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales_india": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/Iopen-enquiries', methods=['GET'])
def get_open_enquiries_india():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM enquiryreportindiacsv 
                WHERE `Enquiry status` = 'Pending' 
                  AND `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries_india": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/Itotal-fresh-enquiries', methods=['GET'])
def get_total_fresh_enquiries_india():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_fresh_enquiries
                FROM enquiryreportindiacsv 
                WHERE `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No fresh enquiries found"}), 404

        return jsonify({"total_fresh_enquiries_india": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Fresh Enquiry data for Global  page

@fresh_blueprint.route('/Gdealers', methods=['GET'])
def get_unique_dealers_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers_global": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fresh_blueprint.route('/Gsales', methods=['GET'])
def get_total_sales_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry status` = 'Closed' 
                  AND `Customer code` IS NOT NULL
                  AND `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales_global": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fresh_blueprint.route('/Gopen-enquiries', methods=['GET'])
def get_open_enquiries_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry status` = 'Pending' 
                  AND `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries_global": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fresh_blueprint.route('/Gtotal-fresh-enquiries', methods=['GET'])
def get_total_fresh_enquiries_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_fresh_enquiries
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry Division` = 'Fresh Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No fresh enquiries found"}), 404

        return jsonify({"total_fresh_enquiries_global": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fresh_blueprint.route('/unique-dealers/country/fresh/global', methods=['GET'])
def get_unique_dealers_per_global():
    try:
        with connect_db() as conn:
            query = """
SELECT 
    Country, 
    COUNT(DISTINCT `Dealer code`) AS unique_dealers
FROM 
    enquiryreportglobalcsv
GROUP BY 
    Country;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No dealer data found for fresh enquiries"}), 404

        return jsonify({"fresh_enquiry_unique_dealers_global": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@fresh_blueprint.route('/product-sales/country-wise/global', methods=['GET'])
def get_product_sales_country_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `Country`, 
                    `Products interested`, 
                    COUNT(*) AS `Total Sales`
                FROM 
                    enquiryreportglobalcsv
                GROUP BY 
                    `Country`, 
                    `Products interested`
                ORDER BY 
                    `Country`, 
                    `Total Sales` DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"country_product_sales_global": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fresh_blueprint.route('/enquiry-types/Country/global', methods=['GET'])
def get_enquiry_types_country_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `Country` AS country,
                    `Products interested` AS product_name,
                    `Enquiry type` AS enquiry_type,
                    COUNT(*) AS enquiry_count
                FROM 
                    enquiryreportglobalcsv
                WHERE
                    `Enquiry division` = 'Fresh Enquiry'
                GROUP BY 
                    `Country`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `Country`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"country_global_enquiry_types": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fresh_blueprint.route('/enquiry-types/Country-wise/Global/converted', methods=['GET'])
def get_enquiry_types_converted_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
                    `Country` AS country,
                    `Products interested` AS product_name,
                    `Enquiry type` AS enquiry_type,
                    COUNT(*) AS enquiry_count
                FROM 
                    enquiryreportglobalcsv
                WHERE
                    `Enquiry division` = 'Fresh enquiry'
                    AND `Enquiry status` = 'Closed'
                GROUP BY 
                    `Country`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `Country`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"converted_enquiry_types_global": df.to_dict(orient='records')}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Fresh Enquiry data for Analysis page

@fresh_blueprint.route('/product-sales/monthly/fresh', methods=['GET'])
def get_monthly_product_sales_fresh():
    try:
        with connect_db() as conn:
            query = """
                SELECT 
    DATE_FORMAT(`Enquiry date`, '%Y-%m') AS month,
    `Products interested` AS product,
    COUNT(*) AS total_sales
FROM (
    SELECT `Enquiry date`, `Products interested`, `Enquiry Division` FROM enquiryreportindiacsv
    UNION ALL
    SELECT `Enquiry date`, `Products interested`, `Enquiry Division` FROM enquiryreportglobalcsv
) AS combined_data
WHERE `Enquiry Division` = 'Fresh Enquiry'
GROUP BY 
    DATE_FORMAT(`Enquiry date`, '%Y-%m'),
    `Products interested`
ORDER BY 
    month ASC, product;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No fresh enquiry product sales data found"}), 404

        return jsonify({"monthly_fresh_product_sales": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

