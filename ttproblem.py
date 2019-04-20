import psycopg2
from flask import Flask
from flask_restplus import Resource, Api


app = Flask(__name__)
api = Api(app)


@api.route('/organizations')
class organizations(Resource):
    return_code = 200

    @staticmethod
    def generate_query(category, city, Orderby, Direction):
        # generate the query string
        query_string = "SELECT id, name, city, state, postal, category FROM organizations"
        #   add a WHERE if we are filtering
        if category is not None or city is not None:
            query_string += " WHERE"
        #   add the category filter
        if category is not None:
            query_string += " category = '{}'".format(category)
        #   add the city filter
        if city is not None:
            if category is not None:
                query_string += " AND"
            query_string += " city = '{}'".format(city)
        #   add ordering if called for
        if Orderby is not None:
            # TODO: fix the data on import/input so we don't have to trim in the query
            query_string += " ORDER BY REPLACE({},' ','')".format(Orderby)
            #   add direction if called for, default is ASC
            if Direction is not None:
                if Direction == "DSC":
                    query_string += " DESC"
                else:
                    query_string += " ASC"

        return query_string

    def query_db(self, query_string, db_connection_string):
        # connect to the DB
        conn = None
        output = None
        try:
            conn = psycopg2.connect(db_connection_string)
        except psycopg2.Warning as e:
            print("Warning while connecting to the database: {}".format(e))
        except psycopg2.Error as e:
            print("Error while connecting to the database: {} {}".format(e.pgcode, e.pgerror))
            self.return_code = 500
            return None

        try:
            cur = conn.cursor()

            # execute the query
            cur.execute(query_string)

            # stuff the query into an object so we can return it
            row = cur.fetchone()
            output = {'organizations': []}

            # add each row to the dict
            while row is not None:
                print("{}".format(row).encode('utf-8'))
                output['organizations'].append(
                    {'id': row[0], 'name': row[1], 'city': row[2], 'state': row[3], 'postal': row[4], 'category': row[5]})
                row = cur.fetchone()
        except psycopg2.Warning as e:
            print("Warning while executing the query: {}".format(e))
        except psycopg2.Error as e:
            print("Error while executing the query: {} {}".format(e.pgcode, e.pgerror))
            self.return_code = 500

        return output

    # define the arguments
    parser = api.parser()
    parser.add_argument("category", type=str, help='Organization category for filtering results [optional]')
    parser.add_argument("city", type=str, help='Organization city for filtering results [optional]')
    parser.add_argument("Orderby", type=str, help='category or city for sorting results [optional]')
    parser.add_argument("Direction", type=str, help='ASC or DSC to specify direction to order results [optional]')

    @api.doc('filter, sort and list organizations')
    @api.response(200, 'Success')
    @api.response(404, 'Failed to find any organizations that meet the requested parameters')
    @api.response(500, 'Failed to connect to the organizations data base')
    @api.expect(parser)
    def get(self):
        # parse the arguments
        args = self.parser.parse_args()

        # see what was passed in
        print("{} {} {} {}".format(args.get('category'), args.get('city'), args.get('Orderby'), args.get('Direction')))

        # print the query for debugging
        query_string = self.generate_query(args.get('category'), args.get('city'), args.get('Orderby'), args.get('Direction'))
        print(query_string)

        output = self.query_db(query_string, "host=localhost dbname=postgres user=postgres password=superduper")

        if output is None or output.get('organizations') is None or len(output['organizations']) == 0:
            self.return_code = 404

        # return the output from the query, defaults 200 for the return code
        return output, self.return_code


if __name__ == '__main__':
    # start the flask server
    app.run(host='0.0.0.0', port='7777')
