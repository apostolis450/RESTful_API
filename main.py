from flask import Flask
from flask_restful import Api,Resource, reqparse ,abort, fields, marshal_with
from flask_sqlalchemy import  SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model): #define the model of video for the db
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False) #100 stands for 'max # of characters'
	views = db.Column(db.Integer,nullable=False)
	likes = db.Column(db.Integer,nullable=False)

	def __repr__(self):
		return f"Video(name={name}, views={views}, likes={likes})" # f-string


#### db.create_all() # ----> creates the database, run it only once!

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video",  required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")


resource_fields = {
	'id'   : fields.Integer,
	'name' : fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):

	@marshal_with(resource_fields) #serialize db data into json format data 
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="No record for given id..")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()

		result = VideoModel.query.filter_by(id=video_id).first()
		if result:	#video id column has unique values for each row
			abort(409, message="Video id already exists..")

		Video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(Video)
		db.session.commit()
		return Video, 201


	@marshal_with(resource_fields)
	def patch(self, video_id):
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		
		if not result:	
			abort(404, message="Video doesn't exist,cannot update")
		
		if  args['name']  :
			result.name = args['name']
		if  args['views'] :
			result.name = args['views']
		if  args['likes'] :
			result.name = args['likes']


		db.session.commit()


	def delete (self, video_id):
		abort_if_not_exist(video_id)
		del videos[video_id]
		return '',204

api.add_resource(Video, "/video/<int:video_id>") #add the resource above and link it with a url


if __name__ == "__main__": 
	app.run(debug=True)

