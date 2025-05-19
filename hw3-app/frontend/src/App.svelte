<script lang="ts">
    import { onMount } from 'svelte';
    
    let currentDate = $state('');
    let apiKey = $state('');
    let dataObj: any;
    
    let artTitle = $state(['', '', '', '']);
    let artAbstract =  $state(['', '', '', '']);
    let artImage =  $state(['', '', '', '']);
    let artCaption = $state(['', '', '', '']);
    
    let loginpopup = $state(false);
    let loggedIn = $state(false);
    let commenting = $state(false);
    let account = $state("Log In");
    let user = $state("");
    let commenttitle = $state("");
    
    async function handleLogin() {
        const authUrl = 'http://localhost:8000/login';
        window.location.href = authUrl;

    }

    function openUserInfo() {
        let userinfoElement = document.getElementById("userinfo");
        if (userinfoElement) {
            userinfoElement.style.display = "block";
        }
    }

    function closeUserInfo() {
        let userinfoElement = document.getElementById("userinfo");
        if (userinfoElement) {
            userinfoElement.style.display = "none";
        }
    }

    function openComment(title: string) {
        commenttitle = title
        let commentsElement = document.getElementById("commentbox");
        if (commentsElement) {
            commentsElement.style.display = "block";
        }
    }

    function closeComment() {
        let commentsElement = document.getElementById("commentbox");
        if (commentsElement) {
            commentsElement.style.display = "none";
        }
        
    }
    function handleSubmit(event: Event) {
        event.preventDefault();
        createComment(commentTitle, commentText, userEmail);
    }

    let commentTitle = $state("");
    let commentText = $state("");
    let userEmail = $state("");

    async function createComment(article: string, comment: string, email: string) {
        let commentsElement = document.getElementById("commentbox");
        if (commentsElement) {
            await fetch('/api/comments', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    article_id: article,
                    comment_text: comment,
                    user: email,
                })
            });
        }
    }
     
    // onMount(() => {
    //     const currurl = window.location.href;
    //     if (currurl.includes("user")) {
    //         loggedIn = true;
    //         account = "Account";
    //     }
    // });

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

    
    // onMount(async () => {
    // try {
    //     const res = await fetch('/api/key');
    //     const data = await res.json();
    //     apiKey = data.apiKey;

    //     if (apiKey) {
    //             execute();
    //     }
    // } catch (error) {
    //     console.error('Failed to fetch API key:', error);
    // }
    // });

    async function execute() {
        const url = `/api/articles`; 
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

    function checkLogIn() {
        const currurl = window.location.href;
        if (currurl.includes("user")) {
            loggedIn = true;
            account = "Account";
            user = currurl.slice(currurl.indexOf('user=') + 5);
        } else {
            loggedIn = false;
            account = "Log In";
        }
    }

    function logout() {
        window.location.href = "http://localhost:5173";
    }

    onMount(() => {
        checkLogIn();
        window.addEventListener("popstate", checkLogIn);
        return () => {
            window.removeEventListener("popstate", checkLogIn);
        };
    });

    execute();

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
                 {#if loggedIn}
                  <button class = "account" onclick={openUserInfo}> {account} </button>
                 {:else}
                  <button class = "login" onclick={handleLogin}> {account} </button>
                 {/if}
            </div>
          </div>
{#if loggedIn}
        <div class="userinfodarkener" id = "userinfo">
            <div class = "userinfocontainer">
                <div class="userspacer"> </div>
                    <div class="userinfobar">
                    <h1>
                        <span class="username">{user}</span>
                    </h1>
                    <button class="account" onclick={closeUserInfo} aria-label="closeUserInfo"> Close User Info </button>
                    <button class="account" onclick={logout} aria-label="logout"> Logout </button>
                    </div>
                </div>
        </div>              
 {/if}

        <div class="commentinfodarkener" id = "commentbox">
            <div class = "commentinfocontainer">
                <div class="commentspacer"> </div>
                    <div class="commentinfobar">
                    <h1>
                        <span class="commentinfo">Comment Section for {commenttitle}</span>
                    </h1>
                    <form onsubmit={handleSubmit}>
                        <label for="commenttext">Comment</label>
                        <input id="commenttext" name="commenttext" bind:value={commentText} required>
                        
                        <button type="submit" class="account">Submit</button>

                    </form>
                    <button class="account" onclick={closeComment} aria-label="closeUserInfo"> CLOSE COMMENTS </button>
                    </div>
                </div>
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
                  <p>{artAbstract[3]}</p>
                    <div class = "buttondiv">  
                        <button class="commentbutton" onclick={() => openComment(artTitle[3])} id="{artTitle[3]}" aria-label="Comment for {artTitle[3]}">
                            <div class="css-1mlnk6q">
                            <svg width="21" height="18" viewBox="0 0 21 18" class="css-2urdiw">
                                <path d="m14.52 17.831-5.715-4.545H2.4a1.468 1.468 0 0 1-1.468-1.469V1.894A1.471 1.471 0 0 1 2.4.405h16.583a1.469 1.469 0 0 1 1.469 1.469v9.923a1.469 1.469 0 0 1-1.47 1.47H14.58l-.06 4.564ZM2.4 1.645a.228.228 0 0 0-.228.229v9.923a.228.228 0 0 0 .228.229h6.811l4.06 3.235v-3.235h5.652a.228.228 0 0 0 .229-.229V1.874a.228.228 0 0 0-.229-.229H2.4Z" fill="#121212" fill-rule="nonzero"></path>
                            </svg>
                            </div>
                        </button>
                    </div>
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
                  <div class = "buttondiv">  
                        <button class="commentbutton" onclick={() => openComment(artTitle[1])} id="{artTitle[1]}" aria-label="Comment for {artTitle[1]}">
                            <div class="css-1mlnk6q">
                            <svg width="21" height="18" viewBox="0 0 21 18" class="css-2urdiw">
                                <path d="m14.52 17.831-5.715-4.545H2.4a1.468 1.468 0 0 1-1.468-1.469V1.894A1.471 1.471 0 0 1 2.4.405h16.583a1.469 1.469 0 0 1 1.469 1.469v9.923a1.469 1.469 0 0 1-1.47 1.47H14.58l-.06 4.564ZM2.4 1.645a.228.228 0 0 0-.228.229v9.923a.228.228 0 0 0 .228.229h6.811l4.06 3.235v-3.235h5.652a.228.228 0 0 0 .229-.229V1.874a.228.228 0 0 0-.229-.229H2.4Z" fill="#121212" fill-rule="nonzero"></path>
                            </svg>
                            </div>
                        </button>
                    </div>
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
                  <div class = "buttondiv">  
                        <button class="commentbutton" onclick={() => openComment(artTitle[2])} id="{artTitle[2]}" aria-label="Comment for {artTitle[2]}">
                            <div class="css-1mlnk6q">
                            <svg width="21" height="18" viewBox="0 0 21 18" class="css-2urdiw">
                                <path d="m14.52 17.831-5.715-4.545H2.4a1.468 1.468 0 0 1-1.468-1.469V1.894A1.471 1.471 0 0 1 2.4.405h16.583a1.469 1.469 0 0 1 1.469 1.469v9.923a1.469 1.469 0 0 1-1.47 1.47H14.58l-.06 4.564ZM2.4 1.645a.228.228 0 0 0-.228.229v9.923a.228.228 0 0 0 .228.229h6.811l4.06 3.235v-3.235h5.652a.228.228 0 0 0 .229-.229V1.874a.228.228 0 0 0-.229-.229H2.4Z" fill="#121212" fill-rule="nonzero"></path>
                            </svg>
                            </div>
                        </button>
                    </div>
                  
              </article>
          </div>
  
  </main>

