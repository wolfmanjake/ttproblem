import psycopg2
from flask import Flask
from flask_restful import Api, Resource, reqparse
import json


class organizations(Resource):
    def get (self):
        # parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument("category")
        parser.add_argument("city")
        parser.add_argument("Orderby")
        parser.add_argument("Direction")
        args = parser.parse_args()

        # see what was passed in
        print("{} {} {} {}".format(args.get('category'), args.get('city'), args.get('Orderby'), args.get('Direction')))

        # connect to the DB
        conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=superduper")
        cur = conn.cursor()

        # generate the query string
        query_string = "SELECT id, name, city, state, postal, category FROM organizations"
        #   add a WHERE if we are filtering
        if args.get('category') is not None or args.get('city') is not None:
            query_string += " WHERE"
        #   add the category filter
        if args.get('category') is not None:
            query_string += " category = '{}'".format(args.get('category'))
        #   add the city filter
        if args.get('city') is not None:
            if args.get('category') is not None:
                query_string += " AND"
            query_string += " city = '{}'".format(args.get('city'))
        #   add ordering if called for
        if args.get('Orderby') is not None:
            # TODO: fix the data on import/input so we don't have to trim in the query
            query_string += " ORDER BY REPLACE({},' ','')".format(args.get('Orderby'))
            #   add direction if called for, default is ASC
            if args.get('Direction') is not None:
                if args.get('Direction') == "DSC":
                    query_string += " DESC"
                else:
                    query_string += " ASC"

        # print the query for debugging
        print(query_string)

        # execute the query
        cur.execute(query_string)

        # stuff the query into an object so we can return it
        row = cur.fetchone()
        output = {'organizations': []}

        # add each row to the dict
        while row is not None:
            print("{}".format(row).encode('utf-8'))
            output['organizations'].append({'id': row[0], 'name': row[1], 'city': row[2], 'state': row[3], 'postal': row[4], 'category': row[5]})
            row = cur.fetchone()

        # dump it to a string and return it
        return json.dumps(output)


# start the flask server
app = Flask(__name__)
api = Api(app)
api.add_resource(organizations, "/organizations")
app.run(host='0.0.0.0', port='7777')