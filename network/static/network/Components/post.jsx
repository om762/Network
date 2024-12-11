function Post() {
  return (
    <div>
      <div className="post-container">
        <div className="profile-info">
          <div className="profile-letter">
            <span>K</span>
          </div>
          <div className="user-info">
            <div>
              <span><a href="user-profile-url">Kashish </a></span>
              ·
              <span><a className="follow-link" href="follow"> Follow</a></span>
            </div>
            <div className="profile-time-div">
              <span>19 hours ago</span>
            </div>
          </div>
        </div>
        <div className="post-content-div">
          Love you :💞
        </div>
      </div>
    </div>
  )
}

function App() {
  return <Post />;
}

ReactDOM.createRoot(document.getElementById('app')).render(<App />);