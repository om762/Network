function Post() {
  return (
    <div>
      <div class="post-container">
        <div class="profile-info">
          <div class="profile-letter">
            <span>K</span>
          </div>
          <div class="user-info">
            <div>
              <span><a href="user-profile-url">Kashish </a></span>
              ·
              <span><a class="follow-link" href="follow"> Follow</a></span>
            </div>
            <div class="profile-time-div">
              <span>19 hours ago</span>
            </div>
          </div>
        </div>
        <div class="post-content-div">
          Love you :💞
        </div>
      </div>
    </div>
  )
}

function App() {
  return <Post />;
}

ReactDOM.render(<App />, document.querySelector('#app'));