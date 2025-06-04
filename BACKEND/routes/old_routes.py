from flask import Blueprint, jsonify
from database import connect_db
import pandas as pd

old_blueprint = Blueprint('old_api', __name__)


# Routing for the API for Old Enquiry data
@old_blueprint.route('/dealers_old', methods=['GET'])
def get_unique_dealers_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM (
                    SELECT `Dealer code` FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'
                    UNION
                    SELECT `Dealer code` FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'
                ) AS combined_dealers;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers_old": int(df.iloc[0, 0])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/sales_old', methods=['GET'])
def get_total_sales_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM (
                    SELECT `Customer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry status` = 'Closed' 
                      AND `Customer code` IS NOT NULL
                      AND `Enquiry Division` = 'Old Enquiry'

                    UNION ALL

                    SELECT `Customer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry status` = 'Closed' 
                      AND `Customer code` IS NOT NULL
                      AND `Enquiry Division` = 'Old Enquiry'
                ) AS all_sales;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/open-enquiries_old', methods=['GET'])
def get_open_enquiries_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM (
                    SELECT `Dealer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry status` = 'Pending' 
                      AND `Enquiry Division` = 'Old Enquiry'

                    UNION ALL

                    SELECT `Dealer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry status` = 'Pending' 
                      AND `Enquiry Division` = 'Old Enquiry'
                ) AS all_open_enquiries;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/total-old-enquiries', methods=['GET'])
def get_total_old_enquiries():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_old_enquiries
                FROM (
                    SELECT `Dealer code` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'

                    UNION ALL

                    SELECT `Dealer code` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'
                ) AS all_old_enquiries;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No old enquiries found"}), 404

        return jsonify({"total_old_enquiries": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@old_blueprint.route('/enquiry-types/old', methods=['GET'])
def get_old_enquiry_type_counts():
    try:
        with connect_db() as conn:
            query = """
                SELECT `Enquiry type`, COUNT(*) AS total
                FROM (
                    SELECT `Enquiry type` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'

                    UNION ALL

                    SELECT `Enquiry type` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'
                ) AS combined_types
                GROUP BY `Enquiry type`
                ORDER BY total DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry type data found"}), 404

        return jsonify({"Old_enquiry_types": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@old_blueprint.route('/enquiry-sources/old', methods=['GET'])
def get_old_enquiry_sources():
    try:
        with connect_db() as conn:
            query = """
                SELECT `Source`, COUNT(*) AS total
                FROM (
                    SELECT `Source` 
                    FROM enquiryreportindiacsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'

                    UNION ALL

                    SELECT `Source` 
                    FROM enquiryreportglobalcsv 
                    WHERE `Enquiry Division` = 'Old Enquiry'
                ) AS combined_sources
                GROUP BY `Source`
                ORDER BY total DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No source data found for fresh enquiries"}), 404

        return jsonify({"old_enquiry_sources": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Old Enquiry data for India  page
@old_blueprint.route('/unique-dealers/State/old', methods=['GET'])
def get_unique_dealers_per_state_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT State, COUNT(*) AS UniqueDealers
                FROM (
                    SELECT `Dealer code`, MIN(State) AS State
                    FROM enquiryreportindiacsv
                    WHERE `Enquiry Division` = 'Old enquiry'
                    GROUP BY `Dealer code`
                ) AS unique_dealers
                GROUP BY State
                ORDER BY UniqueDealers DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No dealer data found for old enquiries"}), 404

        return jsonify({"old_enquiry_unique_dealers": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/product-sales/state-wise/India/old', methods=['GET'])
def get_product_sales_state_wise_old():
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

        return jsonify({"state_wise_product_sales_old": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@old_blueprint.route('/enquiry-types/state-wise/India/old', methods=['GET'])
def get_enquiry_types_state_wise_old():
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
                    `Enquiry division` = 'Old Enquiry'
                GROUP BY 
                    `State`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `State`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"state_wise_enquiry_types_old": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@old_blueprint.route('/enquiry-types/state-wise/India/converted/old', methods=['GET'])
def get_enquiry_types_converted_old():
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
                    `Enquiry division` = 'Old enquiry'
                    AND `Enquiry status` = 'Closed'
                GROUP BY 
                    `State`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `State`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"converted_enquiry_types_old": df.to_dict(orient='records')}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/Idealers', methods=['GET'])
def get_unique_dealers_india_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM enquiryreportindiacsv 
                WHERE `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers_india_old": int(df.iloc[0, 0])})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/Isales', methods=['GET'])
def get_total_sales_india_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM enquiryreportindiacsv 
                WHERE `Enquiry status` = 'Closed' 
                  AND `Customer code` IS NOT NULL
                  AND `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales_india_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/Iopen-enquiries/old', methods=['GET'])
def get_open_enquiries_india_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM enquiryreportindiacsv 
                WHERE `Enquiry status` = 'Pending' 
                  AND `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries_india_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/Itotal-old-enquiries', methods=['GET'])
def get_total_old_enquiries_india():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_old_enquiries
                FROM enquiryreportindiacsv 
                WHERE `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No old enquiries found"}), 404

        return jsonify({"total_old_enquiries_india": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Old Enquiry data for Global  page

@old_blueprint.route('/Gdealers/old', methods=['GET'])
def get_unique_dealers_global_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(DISTINCT `Dealer code`) AS total_unique_dealers 
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"unique_dealers_global_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@old_blueprint.route('/Gsales/old', methods=['GET'])
def get_total_sales_global_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_sales
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry status` = 'Closed' 
                  AND `Customer code` IS NOT NULL
                  AND `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No sales data found"}), 404

        return jsonify({"total_sales_global_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@old_blueprint.route('/Gopen-enquiries/old', methods=['GET'])
def get_open_enquiries_global_old():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_open_enquiries
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry status` = 'Pending' 
                  AND `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No open enquiries found"}), 404

        return jsonify({"total_open_enquiries_global_old": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@old_blueprint.route('/Gtotal-old-enquiries', methods=['GET'])
def get_total_old_enquiries_global():
    try:
        with connect_db() as conn:
            query = """
                SELECT COUNT(*) AS total_fresh_enquiries
                FROM enquiryreportglobalcsv 
                WHERE `Enquiry Division` = 'Old Enquiry';
            """
            df = pd.read_sql_query(query, conn)

        if df.empty or df.iloc[0, 0] is None:
            return jsonify({"error": "No old enquiries found"}), 404

        return jsonify({"total_old_enquiries_global": int(df.iloc[0, 0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@old_blueprint.route('/unique-dealers/country/old/global', methods=['GET'])
def get_unique_dealers_per_global_old():
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
            return jsonify({"error": "No dealer data found for old enquiries"}), 404

        return jsonify({"old_enquiry_unique_dealers_global": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@old_blueprint.route('/product-sales/country-wise/global/old', methods=['GET'])
def get_product_sales_country_global_old():
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

        return jsonify({"country_product_sales_global_old": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@old_blueprint.route('/enquiry-types/Country/global/old', methods=['GET'])
def get_enquiry_types_country_global_old():
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
                    `Enquiry division` = 'Old Enquiry'
                GROUP BY 
                    `Country`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `Country`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"country_global_enquiry_types_old": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@old_blueprint.route('/enquiry-types/Country-wise/Global/converted/old', methods=['GET'])
def get_enquiry_types_converted_global_old():
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
                    `Enquiry division` = 'Old enquiry'
                    AND `Enquiry status` = 'Closed'
                GROUP BY 
                    `Country`, `Products interested`, `Enquiry type`
                ORDER BY 
                    `Country`, `Products interested`, enquiry_count DESC;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No enquiry data found"}), 404

        return jsonify({"converted_enquiry_types_global_old": df.to_dict(orient='records')}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Routing for the API for Old Enquiry data for Analysis page

@old_blueprint.route('/product-sales/monthly/old', methods=['GET'])
def get_monthly_product_sales_old():
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
WHERE `Enquiry Division` = 'Old Enquiry'
GROUP BY 
    DATE_FORMAT(`Enquiry date`, '%Y-%m'),
    `Products interested`
ORDER BY 
    month ASC, product;
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return jsonify({"error": "No old enquiry product sales data found"}), 404

        return jsonify({"monthly_old_product_sales": df.to_dict(orient='records')})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

