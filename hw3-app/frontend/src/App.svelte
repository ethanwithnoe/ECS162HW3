<script lang="ts">
    import { onMount } from 'svelte';
    
    let currentDate = $state('');
    let apiKey = $state('');
    let dataObj: any;
    let artTitle = $state(['', '', '', '']);
    let artAbstract =  $state(['', '', '', '']);
    let artImage =  $state(['', '', '', '']);
    let artCaption = $state(['', '', '', '']);


    async function handleLogin() {
        const authUrl = 'http://localhost:8000/login';
        window.location.href = authUrl;
    }


    onMount(() => {
        const utcTime = new Date();
        const settings = {
            weekday: 'long' as 'long',
            year: 'numeric' as 'numeric',
            month: 'long' as 'long',
            day: 'numeric' as 'numeric',
        };
        currentDate = utcTime.toLocaleDateString("en-US", settings);
    });

    
    onMount(async () => {
    try {
        const res = await fetch('/api/key');
        const data = await res.json();
        apiKey = data.apiKey;

        if (apiKey) {
                execute();
        }
    } catch (error) {
        console.error('Failed to fetch API key:', error);
    }
    });

    async function execute() { 
        const url = `https://api.nytimes.com/svc/search/v2/articlesearch.json?q="Davis CA""U.C. Davis"&api-key=${apiKey}`; 
        //const url = `https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=%22Davis%20California%22%20%22Yolo%20County%22%20%22Sacramento%22&q=%22Davis%20California%22%20%22University%20of%20California%2C%20Davis%22%20&sort=relevance&api-key=${apiKey}`;
        const options = {
            method: "GET",
            headers: {
                "Accept": "application/json",
            },
        };
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error();
            }
            const data = await response.json();
            console.log(data);
            dataObj = data;
            for (let i = 0; i < artTitle.length; i++) {
                artTitle[i] = dataObj.response.docs[i].headline.main;
                artAbstract[i] = dataObj.response.docs[i].abstract;
                artImage[i] = dataObj.response.docs[i].multimedia.default.url;
                artCaption[i] = dataObj.response.docs[i].multimedia.caption;
            }
            
        } catch (error) {
            console.error();
        }
    }

    let loginpopup = $state(false);
    let loggedIn = $state(false);
    let commenting = $state(false);

    function openForm() {
        document.getElementById("myForm").style.display = "block";
    }

    function closeForm() {
        document.getElementById("myForm").style.display = "none";
    }

  </script>
  
  <main>
          <link rel="stylesheet" href="hw1.css">
          <title>The New York Times</title>
  
          <div class = "header">
            <span class="time" id="currTime">{currentDate}</span>
              <div class="titlebox">
                      <img src = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/NewYorkTimes.svg/2560px-NewYorkTimes.svg.png" 
                      alt="New York Times Logo" 
                      height ="159" 
                      width =  "1080" 
                      class = title>
              </div>
              <div class = "spacer">
                <button class = "login" onclick={handleLogin}> Log In </button>
            </div>
              
          </div>

          <!-- A button to open the popup form -->
          <button class="open-button" onclick={openForm}>Open Form</button>
          <!-- The form -->
           <div class="form-popup" id="myForm">
            <form action="/action_page.php" class="form-container">
                <h1>Login</h1>

                <label for="email"><b>Email</b></label>
                <input type="text" placeholder="Enter Email" name="email" required>

                <label for="psw"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="psw" required>

                <button type="submit" class="btn">Login</button>
                <button type="button" class="btn cancel" onclick={closeForm}>Close</button>
            </form>
            </div>

          
          <div class="secondline">
          </div>
          <div class="container" id="container-1">
              <article class="article art1">
                  <header>
                      <h2>{artTitle[3]}</h2>
                  </header>
                  <figure>
                      <img src = "{artImage[3]}" 
                      alt ="{artCaption[3]}"
                      height="500"
                      width="800"
                      class="image img1">
                  </figure>
                  <p>{artAbstract[0]}</p>
      
              </article>
              <article class="article art2">
                  <header>
                      <h2>{artTitle[1]}</h2>
                  </header>
                  <figure>
                      <img src = "{artImage[1]}" 
                      alt ="{artCaption[1]}"
                      height="563"
                      width="1000"
                      class="image img2">
                  </figure>
                  <p>{artAbstract[1]}</p>
              </article>
              <article class="article art3">
                  <header>
                      <h2>{artTitle[2]}</h2>
                  </header>
                  <figure>
                      <img src = "{artImage[2]}" 
                      alt = "{artCaption[2]}"
                      height="1080"
                      width="1920"
                      class="image img3">
                  </figure>
                  <p>{artAbstract[2]}</p>
                  
              </article>
          </div>
  
  </main>
  
  