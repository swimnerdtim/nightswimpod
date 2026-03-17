import { Link } from 'react-router-dom';
import { useState } from 'react';
import EpisodeCard from '../components/EpisodeCard';
import episodes from '../data/episodes.json';
import './Home.css';

function Home() {
  const latestEpisode = episodes[0];
  const highlightEpisodes = episodes.slice(0, 6);
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState(''); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setMessage('');

    try {
      const response = await fetch('https://swimnerd-server-signup.onrender.com/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setStatus('success');
        setMessage('Thanks for subscribing! 🎉');
        setEmail('');
      } else {
        setStatus('error');
        setMessage(data.error || 'Something went wrong. Please try again.');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Network error. Please try again.');
      console.error('Signup error:', error);
    }
  };

  return (
    <div className="home">
      {/* Latest Episode Section */}
      <section className="section latest-episode-section">
        <div className="container">
          <h1 className="section-title">LATEST EPISODE</h1>
          <p className="section-subtitle">When the pool lights go out, the real talk begins</p>
          
          <div className="video-container">
            <iframe
              src={`https://www.youtube.com/embed/${latestEpisode.youtubeId}`}
              title={latestEpisode.title}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
          
          <Link to="/episodes" className="watch-all-link">
            <span>▶</span> Watch All Swimming Podcast Episodes
          </Link>
        </div>
      </section>

      {/* Episode Highlights Section */}
      <section className="section highlights-section">
        <div className="container">
          <h2 className="section-title">EPISODE HIGHLIGHTS</h2>
          <p className="section-subtitle">
            Unfiltered swim culture – NCAA battles, Olympic tea, and pool-deck chaos
          </p>
          
          <div className="grid-3">
            {highlightEpisodes.map(episode => (
              <EpisodeCard key={episode.id} episode={episode} />
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section className="section about-section">
        <div className="container">
          <h2 className="section-title">ABOUT THE SHOW</h2>
          <p className="section-subtitle">
            Unfiltered swim culture from two Black swimmers who've seen it all
          </p>
          
          <div className="about-content">
            <div className="about-text">
              <h3>MEET YOUR HOSTS</h3>
              <p>
                <strong style={{color: 'var(--green-bright)'}}>Dax Hill</strong> (NCAA champ, Texas Longhorns legend, high-performance technique guru @BryoIo) & 
                <strong style={{color: 'var(--green-bright)'}}> Elvis Burrows</strong> (Bahamian Olympian, national record holder, founder of Burrow's Best swimmer hair and skin care). 
                Night Swim is unfiltered swim culture every week.
              </p>
              <p>
                From USA Swimming's gay pride drama to the Enhanced Games controversy, NCAA battles to Olympic tea – Night Swim covers it all with no scripts and no PR. 
                Just honest takes on the sport we've dedicated our lives to.
              </p>
              <p>
                New episodes weekly. Grab your goggles, hit subscribe, and dive in. 🏊‍♂️ Presented by <strong>Swimnerd</strong>.
              </p>
            </div>
            
            <div className="about-stats">
              <div className="stat-card">
                <div className="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
                  </svg>
                </div>
                <div className="stat-value">NEW</div>
                <div className="stat-label">WEEKLY EPISODES</div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                  </svg>
                </div>
                <div className="stat-value">100%</div>
                <div className="stat-label">SWIMMING FOCUS</div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                  </svg>
                </div>
                <div className="stat-value">GLOBAL</div>
                <div className="stat-label">COMMUNITY</div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/>
                  </svg>
                </div>
                <div className="stat-value">ELITE</div>
                <div className="stat-label">ATHLETES FEATURED</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Subscribe Section */}
      <section className="section subscribe-section">
        <div className="container">
          <h2 className="section-title">SUBSCRIBE NOW</h2>
          <p className="section-subtitle">
            Never miss an episode. Follow us on your favorite platform.
          </p>
          
          <div className="platform-buttons">
            <a href="https://podcasts.apple.com/..." target="_blank" rel="noopener noreferrer" className="platform-button">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/>
              </svg>
              <span>Apple Podcasts</span>
            </a>
            
            <a href="https://www.youtube.com/@nightswimpodcast" target="_blank" rel="noopener noreferrer" className="platform-button">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
              </svg>
              <span>YouTube</span>
            </a>
            
            <a href="https://open.spotify.com/show/..." target="_blank" rel="noopener noreferrer" className="platform-button">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
              </svg>
              <span>Spotify</span>
            </a>
            
            <a href="#" className="platform-button">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
              <span>Other Platforms</span>
            </a>
          </div>
          
          <div className="email-signup">
            <h3>JOIN THE SWIM CREW</h3>
            <p>Get exclusive updates, behind-the-scenes content, and be the first to know about new episodes and special guests.</p>
            <form className="signup-form" onSubmit={handleSubmit}>
              <input 
                type="email" 
                placeholder="Enter your email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={status === 'loading'}
                required 
              />
              <button 
                type="submit" 
                className="btn-primary"
                disabled={status === 'loading'}
              >
                {status === 'loading' ? 'Subscribing...' : 'Subscribe'}
              </button>
            </form>
            {message && (
              <p className={`signup-message ${status}`} style={{
                marginTop: '10px',
                color: status === 'success' ? 'var(--green-bright)' : '#ff6b6b',
                fontWeight: 'bold'
              }}>
                {message}
              </p>
            )}
            <p className="signup-disclaimer">No spam, ever. Unsubscribe anytime.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
