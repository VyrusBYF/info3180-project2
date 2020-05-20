
/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <i class="fas fa-camera" style="margin-right:7px"></i><a class="navbar-brand title" href="#">Photogram</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link class="nav-link" id= "H" to="/"> Home <span class="sr-only">(current)</span></router-link>
          </li>
          <li>
            <router-link class="nav-link" id= "E" to="/explore">Explore</router-link>
          </li>
          <li>
            <router-link class="nav-link" id= "MP" to="/users/${localStorage.getItem('cuser_id')}"> My Profile</router-link>
          </li>
          <li>
            <router-link class="nav-link" id= "LO" to="/logout">Log Out</router-link>
          </li>
        </ul>
      </div>
    </nav>
    `
});
//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

var auth_status = null;
var cuser_id = localStorage.getItem('cuser_id');
var user_id = null;
var users=[];
function chguserid(new_id){
	user_id = new_id;
}
function barchan(){
	if(localStorage.getItem('token')!==null & localStorage.getItem('cuser_id')!==null){
		$("#H").hide();
		$("#R").hide();
		$("#LI").hide();
		$("#P").show();
		$("#MP").show();
		$("#E").show();
		$("#LO").show();
		return true;
	}else{
		$("#H").show();
		$("#R").show();
		$("#LI").show();
		$("#P").hide();
		$("#MP").hide();
		$("#E").hide();
		$("#LO").hide();
		return false;
	}
}


function change(){
        var mybtn = document.getElementById("mybtn");
        var mainbtn = document.getElementById("photo"); //Original Button
        
        mainbtn.click();

}
function text(){
    var mytext = document.getElementById("filemsg");
    var text = document.getElementById('photo').value.split("\\");
    //console.log(text[text.length-1]);

    mytext.innerHTML = text[text.length-1];

}

const Register  = Vue.component('register',{
    template:`
        <div class = "register-card">
            <h1>Register</h1>
            <div class = "regiform">
	            <form id ="regForm" method = "POST" @submit.prevent="register" enctype="multipart/form-data">

	                <label>Username</label><br>
	                <input name="username" type="text"><br><br>
	                
	                <label>Password</label><br>
	                <input name="password" type="password"><br><br>
	                
	                <label>First Name</label><br>
	                <input name="firstname" type="text"><br><br>

	                <label>Last Name</label><br>
	                <input name="lastname" type="text"><br><br>
	                
	                <label>Email</label><br>
	                <input name="email" type="email"><br><br>
	                
	                <label>Locaton</label><br>
	                <input name="location" type="text"><br><br>

	                <label for="bio">Biography</label><br>
	                <textarea name="biography" placeholder="Insert Text Here" id="bio"></textarea><br>

	                <label for="file">Photo</label><br>
	                <input name="photo" type = "file" id="photo" accept="image/png, image/jpeg" onchange="text()" hidden="hidden">
	                <button type="button" id="mybtn" onclick = "change()">Browse</button><span id="filemsg"> No file Chosen...</span><br>

	                <button type= "submit" id="submitbtn"> Submit </button>
	            </form>
            </div>
        </div>
    `,
    created:function(){
        if(barchan()!= false){
        	router.push({name: 'home'});
        }
	},
    data: function(){
        return {
            messages: [],
            error: []
        };
    },
    methods:{
        register: function(){
            let regForm = document.getElementById('regForm');
            let form_data = new FormData(regForm);

            fetch('/api/users/register', {
                method: 'POST',
                body: form_data,
                headers:{
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
                console.log(jsonResponse);
                auth_status = jsonResponse.status;
                if(auth_status == true){
                    router.push({ name: "login"})
                }
                
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
});


const Login     = Vue.component('login',{
    template:`
        <div class = "login-card">
        <h1>Login</h1>
            <div class = "logform">
                <form id ="logIForm" method = "POST" @submit.prevent="login" enctype="multipart/form-data">

                    <label>Username</label><br>
                    <input name="username" type="text"><br><br>
                    
                    <label>Password</label><br>
                    <input name="password" type="password"><br><br>
                    
                    <button type= "submit"> Login </button>
                </form>
            </div>
        </div>

    `,
    created:function(){
        if(barchan()!= false){
        	router.push({name: 'home'});
        }
	},
    data: function(){
        return {
            messages: [],
            error: []
        };
    },
    methods:{
        login: function(){
            let logIForm = document.getElementById('logIForm');
            let form_data = new FormData(logIForm);

            fetch('/api/auth/login', {
                method: 'POST',
                body: form_data,
                headers:{
                    'X-CSRFToken': token

                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
                console.log(jsonResponse);
                jsonResponse.status
                auth_status = jsonResponse.status;
                if(auth_status== true){
                    cuser_id = jsonResponse.user_id;
                    localStorage.setItem('cuser_id', cuser_id);
                    console.log(cuser_id);
                }
                let jwt_token = jsonResponse.token;
                console.log(localStorage);
                localStorage.setItem('token', jwt_token);
                console.info('Token generated and added to localStorage.');
                self.token = jwt_token;

                router.push({name: 'explore'});
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
});


const Logout    = Vue.component('logout',{
    template:`
        <div>
            <h1>Do You Want To Log Out?</h1> 
            <form id ="logOForm"  @submit.prevent="logout">
                <button type= "submit" id="submitbtn"> Log Out </button>
            </form>         
        </div>

    `,
    created:function(){
        let self = this;
        if(barchan()!= true){
        	router.push({name: 'home'});
        }else if(localStorage.getItem('token')!==null){
            self.usertoken=localStorage.getItem('token');   
        }
    },
    data: function(){
        return {
            messages: [],
            error: []
        };
    },
    methods:{
        logout: function(){
            let logOForm = document.getElementById('logOForm');
            let form_data = new FormData(logOForm);
            fetch('/api/auth/logout', {
                method: 'GET',
                headers:{
                    'X-CSRFToken': token,
                    'Authorization': 'Bearer ' + localStorage.getItem('token')

                },
            credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
                console.log(jsonResponse);
                localStorage.removeItem('token');
                console.log('Token removed from localStorage.');
                if(barchan()!= true){
                	router.push({name: 'home'});
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
});


const Explore     = Vue.component('explore',{
    template:`
        <div>
            <router-link class="nav-link" id= "P" to="/posts/new">
            	<button id="exbtn" type="submit" >New Post</button>
            </router-link>
            <ul id="feed"> 
                <li v-for="post in posts">
                    <div class="post-item">
                        <div class="grid1">
            				<router-link id="UP" :to="'/users/' + post.post_uid">
            					<img v-bind:src="post.propic"> {{post.username}}
            				</router-link>  	
                        </div>
                        <div class="grid2">
                             <span id="postpic"><img v-bind:src ="post.photo" alt = "Gaza" class= "image"></span>
                        </div>
                        <div class="grid3">
                            {{ post.caption }}
                        </div>
                        <div class="grid4">
                        	<div v-if="post.liked== 0">
                        		<div :id = "'snotliked'+post.post_id" >
                            		<button class="like-button" v-on:click="plikes(post.post_id,0)"><i class="far fa-heart"></i> {{ post.likes  }} Likes</button>
                        		</div>
                        		<div :id = "'liked'+post.post_id" style ="display: none">
                            		<button class="like-button" v-on:click="plikes(post.post_id,0)"><i class="fas fa-heart liked"></i> {{ post.likes + 1 }} Likes</button>
                        		</div>

                        	</div>
                        	<div v-else>
                        	
                        		<div :id = "'sliked'+post.post_id">
                            		<button class="like-button" v-on:click="plikes(post.post_id,1)"><i class="fas fa-heart liked"></i> {{ post.likes }} Likes</button>
                        		</div>
                        		<div :id = "'notliked'+post.post_id" style ="display: none">
                            		<button class="like-button" v-on:click="plikes(post.post_id,1)"><i class="far fa-heart"></i> {{ post.likes - 1 }} Likes</button>
                        		</div>
                        	</div>
                        </div>
                        <div class="grid4-2">
                            {{ post.created }}
                        </div>
                    </div>
                <br>
                </li>
            </ul>
        </div>
    `,
    created:function(){
        //var exbtn = $('exbtn');
        //exbtn.click();
        //console.log("I work!");
        if(barchan()!= true){
        	router.push({name: 'home'});
        }
        let self = this;
            fetch('/api/posts',{
                method: 'GET',
                headers:{
                    
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
                console.log(jsonResponse);
                users=jsonResponse.users
                self.posts = jsonResponse.posts; 
            })
            .catch(function (error) {
                console.log(error);
            });
    },
    data: function(){
        return{
            posts: []
        };
    },
    methods:{
    	plikes:function (post_id,liked){
    		
			fetch('/api/posts/'+post_id+'/like',{
                method: 'POST',
                headers:{
                    'X-CSRFToken': token,
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message

                if (liked==0) {
                	if (jsonResponse == 0) {
                		$("#snotliked"+post_id.toString()).show();
						$("#liked"+post_id.toString()).hide();
					}else if (jsonResponse == 1) {
                		$("#snotliked"+post_id.toString()).hide();
						$("#liked"+post_id.toString()).show();
					}
				}else if (liked==1) {
                	if (jsonResponse == 0) {
                		$("#notliked"+post_id.toString()).show();
						$("#sliked"+post_id.toString()).hide();
					}else if (jsonResponse == 1) {
                		$("#notliked"+post_id.toString()).hide();
						$("#sliked"+post_id.toString()).show();
					}
				}
		
                
                self.posts = jsonResponse.posts; 
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
});

const Users     = Vue.component('users',{
    template:`
        <div>
            <div class="profile-card">
                <div class="pgrid1">
                    <img v-bind:src= user.pro_pic>
                </div>
                <div class="pgrid2">
                    <span id="fullname"> {{ user.fname }} {{ user.lname }} </span><br><br>
                    {{ user.location }}<br>
                    {{ user.join_date }}<br><br>
                    {{ user.bio }}
                </div>
                <div>
	                <div v-if="user.followed==0">
	                	<div class ="pgrid3" :id = "'snotfollowed'+user.user_id" >
		                	<div class="spgrid1">
			                    {{ posts }}
			                </div>
			                <div class="spgrid2">
			                    {{ followers }}                   
			                </div>
			                <div class="spgrid3">
			                    Posts
			                </div>
			                <div class="spgrid4">
			                    Followers 
			                </div>
		                	<div class="spgrid5">
			                    <button v-on:click="follows(user.user_id,0)"> Follow </button>
			                </div>
			            </div>
			            <div  class ="pgrid3" :id = "'followed'+user.user_id" style ="display: none">
		                	<div class="spgrid1">
			                    {{ posts }}
			                </div>
			                <div class="spgrid2">
			                    {{ followers + 1}}                   
			                </div>
			                <div class="spgrid3">
			                    Posts
			                </div>
			                <div class="spgrid4">
			                    Followers 
			                </div>
		                	<div class="spgrid5">
			                    <button v-on:click="follows(user.user_id,0)"> Following </button>
			                </div>
			            </div>	                
	                </div>
	                <div v-else-if= "user.followed==1">
	                	<div class ="pgrid3" :id = "'sfollowed'+user.user_id">
		                	<div class="spgrid1">
			                    {{ posts }}
			                </div>
			                <div class="spgrid2">
			                    {{ followers }}                   
			                </div>
			                <div class="spgrid3">
			                    Posts
			                </div>
			                <div class="spgrid4">
			                    Followers 
			                </div>
		                	<div class="spgrid5">
			                    <button v-on:click="follows(user.user_id,1)"> Following </button>
			                </div>
			            </div>
			            <div class ="pgrid3" :id = "'notfollowed'+user.user_id" style ="display: none">
		                	<div class="spgrid1">
			                    {{ posts }}
			                </div>
			                <div class="spgrid2">
			                    {{ followers - 1}}                  
			                </div>
			                <div class="spgrid3">
			                    Posts
			                </div>
			                <div class="spgrid4">
			                    Followers 
			                </div>
		                	<div class="spgrid5">
			                    <button v-on:click="follows(user.user_id,1)"> Follow </button>
			                </div>
			            </div>
	                </div>
	                <div v-else>
	                	<div class ="pgrid3">
		                	<div class="spgrid1">
			                    {{ posts }}
			                </div>
			                <div class="spgrid2">
			                    {{ followers }}                   
			                </div>
			                <div class="spgrid3">
			                    Posts
			                </div>
			                <div class="spgrid4">
			                    Followers 
			                </div>
		                </div>
	                </div>
                </div>







               
            </div>
            <ul id="userposts">
                <li v-for= "i in photos.pics">
                    <img v-bind:src= i >
                </li>
            </ul>
        </div>
    `,
    data: function(){
        return{
            user: [],
            posts: 0,
            followers: 0,
            count:0,
            photos: [],
            uid:this.$route.params.user_id
        };
    },
    created:function(){
        if(barchan()!= true){
        	router.push({name: 'home'});
        }
        chguserid(this.uid)
        console.log(this.uid)
        let self = this;
        fetch('/api/users/'+user_id+'/posts', {

            method: 'GET',
            headers:{
                
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
            credentials: 'same-origin'
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
        // display a success message
            console.log(jsonResponse);
            self.user = jsonResponse.user;
            self.posts = jsonResponse.posts;
            self.followers = jsonResponse.followers;
            self.photos = jsonResponse.photos;
        })
        .catch(function (error) {
            console.log(error);
        });
	},
    methods:{
    	follows:function (user_id,followed){
    		
			fetch('/api/users/'+user_id+'/follow',{
                method: 'POST',
                headers:{
                    'X-CSRFToken': token,
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message

                if (followed==0) {
                	if (jsonResponse == 0) {
                		$("#snotfollowed"+user_id.toString()).show();
						$("#followed"+user_id.toString()).hide();
					}else if (jsonResponse == 1) {
                		$("#snotfollowed"+user_id.toString()).hide();
						$("#followed"+user_id.toString()).show();
					}
				}else if (followed==1) {
                	if (jsonResponse == 0) {
                		$("#notfollowed"+user_id.toString()).show();
						$("#sfollowed"+user_id.toString()).hide();
					}else if (jsonResponse == 1) {
                		$("#notfollowed"+user_id.toString()).hide();
						$("#sfollowed"+user_id.toString()).show();
					}
				}
		
                
                self.posts = jsonResponse.posts; 
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }

});

const Posts     = Vue.component('posts',{
    template:`
        <div>
            <h1>New Post</h1>
            <form id ="nPostForm" method = "POST" @submit.prevent="new_post" enctype="multipart/form-data">

                <label for="file">Photo</label><br>
                <input name="photo" type = "file" id="photo" accept="image/png, image/jpeg" onchange="text()" hidden="hidden">
                <button type="button" id="mybtn" onclick = "change()">Browse</button><span id="filemsg"> No file Chosen...</span><br>

                <label for="caption">Caption</label><br>
                <textarea name="caption" placeholder="Insert Text Here" id="bio"></textarea><br>

                <button type= "submit" id="submitbtn"> Submit </button>
            </form>
        </div>
    `,
    created:function(){
        if(barchan()!= true){
        	router.push({name: 'home'});
        }

	},
     data: function(){
        return {
            messages: [],
            error: []
        };
    },
    methods:{
        new_post: function(){
            let nPostForm = document.getElementById('nPostForm');
            let form_data = new FormData(nPostForm);
            console.log("current user is ", cuser_id)
            if (cuser_id != null){
                fetch('/api/users/'.concat(cuser_id,'/posts'), {
                    method: 'POST',
                    body: form_data,
                    headers:{
                        'X-CSRFToken': token,
                        'Authorization': 'Bearer ' + localStorage.getItem('token')
                    },
                    credentials: 'same-origin'
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                    console.log(jsonResponse);
                    router.push({name: 'user', params:{user_id:cuser_id}});
                })
                .catch(function (error) {
                    console.log(error);
                });
            }else{
                console.log("There is no user logged in");
            }
        }
    }
});


const Home = Vue.component('home', {

   	template: `
    <div class="homegrid-outer">
        <div class="homephoto">
            <img src = "https://static.boredpanda.com/blog/wp-content/uploads/2017/07/1-DSC_0555-1c-Liubarto-5977af6e84a8a__880.jpg"> 
        </div>
        <div class = "homegrid-inner">
            <div class="homegrid1 hometitle">
                <i class="fas fa-camera" style="margin-right:7px"></i> <span> Photogram </span>
            </div>
            <div class="homegrid2">
                Share photo of your favorite moments with friends family and the world.
            </div>
            <div class="homegrid3">
            	<router-link id= "R" to="/register">
            		<button class = "regbtn"> Register</button>
            	</router-link>    
            </div>
            <div class="homegrid3-2">
             	<router-link id= "LI" to="/login">
             		<button class="logbtn">Login</button>
             	</router-link>	
            </div>
        </div>
   	 </div>
   	`,
    data: function() {
       return {}
    }
    ,
    created:function(){
        if(localStorage.getItem('token')!==null & localStorage.getItem('cuser_id')!==null){

            barchan(); 
            router.push({name: 'explore'});
            
        }
    }
});


const Upload = Vue.component('upload-form',{
    template: `
        <div>
            <h1>Upload Form</h1>
            <form id ="uploadForm" method = "POST" @submit.prevent="uploadPhoto" enctype="multipart/form-data">
                <label for="desc">Description</label><br>
                <textarea name="description" placeholder="Insert Text Here" id="desc"></textarea><br>

                <label for="file">Photo Upload</label><br>
                <input name="photo" type = "file" id="photo" accept="image/png, image/jpeg" onchange="text()" hidden="hidden">
                <button type="button" id="mybtn" onclick = "change()">Browse</button><span id="filemsg"> No file Chosen...</span><br>

                <button type= "submit" id="submitbtn"> Submit </button>
            </form>
        </div>
  `,
    data: function(){
        return {
            messages: [],
            error: []
        };
    },
    methods:{
        uploadPhoto: function(){
            let uploadForm = document.getElementById('uploadForm');
            let form_data = new FormData(uploadForm);

            fetch('/api/upload', {
                method: 'POST',
                body: form_data,
                headers:{
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
                console.log(jsonResponse);
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }
});

//------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Vue.component('app-footer', {
    template: `
    <footer>
    </footer>
    `
});


const NotFound = Vue.component('not-found', {
    template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
    data: function () {
        return {}
    }
})

// Define Routes
const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: "/", component: Home, name:'home'},
        // Put other routes here
        {path: "/register", component: Register, name:'register'},
        {path: "/login", component: Login , name: "login" },
        {path: "/logout", component: Logout, name: 'logout'},
        {path: "/explore", component: Explore, name: 'explore'},
        {path: "/users/:user_id", component: Users, name:'user'},
        {path: "/posts/new", component: Posts, name:'new post'},

        // This is a catch all route in case none of the above matches
        {path: "*", component: NotFound}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});
barchan();