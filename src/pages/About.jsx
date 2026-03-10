import './About.css';

function About() {
  return (
    <div className="about-page">
      <section className="section">
        <div className="container">
          <div className="about-hero">
            <img src="/logo.png" alt="Night Swim Podcast" className="about-logo" />
            <h1 className="section-title">ABOUT NIGHT SWIM</h1>
            <p className="about-tagline">
              Your weekly destination for everything swimming. From elite athlete interviews to breaking news, 
              training tips, and major event coverage.
            </p>
          </div>
          
          <div className="mission-section">
            <h2 className="mission-title">OUR MISSION</h2>
            <div className="mission-content">
              <div className="mission-text">
                <p className="mission-highlight">
                  When the <span className="highlight-green">pool lights go out</span>, 
                  the <span className="highlight-green">real talk begins</span>. Night Swim Podcast 
                  dives into the depths of swimming with unedited, unrehearsed stories from the pool deck and beyond.
                </p>
                <p>
                  Hosted by former NCAA champion <strong>Dax Hill</strong> and Bahamian Olympian <strong>Elvis Burrows</strong>, 
                  we bring you authentic conversations about the sport we've dedicated our lives to. 
                  From hot takes on the latest competitions to deep dives with elite athletes.
                </p>
                <p>
                  We cover it all: professional swimming news, training insights, athlete nutrition, and the untold 
                  stories of NCAA meets. No PR spin—just two Black swimmers who've been there, saying what everyone else whispers.
                </p>
                <p className="mission-footer">
                  New episodes weekly. Grab your goggles, hit subscribe, and dive in. 
                  🏊‍♂️ Presented by <strong>Swimnerd</strong>.
                </p>
              </div>
              
              <div className="mission-stats">
                <div className="stat-large">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/>
                  </svg>
                  <div className="stat-value">NEW</div>
                  <div className="stat-label">WEEKLY EPISODES</div>
                </div>
                
                <div className="stat-large">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                  </svg>
                  <div className="stat-value">100%</div>
                  <div className="stat-label">SWIMMING FOCUS</div>
                </div>
                
                <div className="stat-large">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                  </svg>
                  <div className="stat-value">GLOBAL</div>
                  <div className="stat-label">COMMUNITY</div>
                </div>
                
                <div className="stat-large">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="var(--green-bright)">
                    <path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/>
                  </svg>
                  <div className="stat-value">ELITE</div>
                  <div className="stat-label">ATHLETES FEATURED</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;
