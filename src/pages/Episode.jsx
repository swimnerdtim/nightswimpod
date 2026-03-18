import { useParams, Link } from 'react-router-dom';
import { useEffect } from 'react';
import episodes from '../data/episodes.json';
import './Episode.css';

function Episode() {
  const { slug } = useParams();
  const episode = episodes.find(ep => ep.id === slug);
  
  useEffect(() => {
    if (episode) {
      // Update page title and meta tags
      document.title = `${episode.title} | Night Swim Podcast`;
      
      // Update meta description
      const metaDesc = document.querySelector('meta[name="description"]');
      if (metaDesc) {
        metaDesc.setAttribute('content', episode.description);
      } else {
        const meta = document.createElement('meta');
        meta.name = 'description';
        meta.content = episode.description;
        document.head.appendChild(meta);
      }
      
      // Update Open Graph tags
      updateMetaTag('og:title', episode.title);
      updateMetaTag('og:description', episode.description);
      updateMetaTag('og:image', episode.thumbnail);
      updateMetaTag('og:url', window.location.href);
      updateMetaTag('og:type', 'video.other');
      
      // Twitter Card
      updateMetaTag('twitter:card', 'player', 'name');
      updateMetaTag('twitter:title', episode.title, 'name');
      updateMetaTag('twitter:description', episode.description, 'name');
      updateMetaTag('twitter:image', episode.thumbnail, 'name');
    }
  }, [episode]);
  
  const updateMetaTag = (property, content, attr = 'property') => {
    let meta = document.querySelector(`meta[${attr}="${property}"]`);
    if (meta) {
      meta.setAttribute('content', content);
    } else {
      meta = document.createElement('meta');
      meta.setAttribute(attr, property);
      meta.setAttribute('content', content);
      document.head.appendChild(meta);
    }
  };
  
  if (!episode) {
    return (
      <div className="episode-page">
        <div className="container">
          <div className="not-found">
            <h1>Episode Not Found</h1>
            <p>Sorry, we couldn't find that episode.</p>
            <Link to="/episodes" className="btn-primary">
              View All Episodes
            </Link>
          </div>
        </div>
      </div>
    );
  }
  
  return (
    <div className="episode-page">
      <section className="section">
        <div className="container">
          <Link to="/episodes" className="back-link">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
            </svg>
            Back to Episodes
          </Link>
          
          <div className="episode-header">
            <p className="episode-date">
              {new Date(episode.publishDate).toLocaleDateString('en-US', { 
                month: 'long', 
                day: 'numeric', 
                year: 'numeric' 
              })}
            </p>
            <h1 className="episode-title-large">{episode.title}</h1>
          </div>
          
          <div className="episode-video">
            <div className="video-container">
              <iframe
                src={`https://www.youtube.com/embed/${episode.youtubeId}`}
                title={episode.title}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
            </div>
          </div>
          
          <div className="episode-details">
            <div className="episode-description-full">
              <h2>About This Episode</h2>
              <p>{episode.description}</p>
              
              {episode.transcript && (
                <div className="episode-transcript">
                  <h2>Episode Transcript</h2>
                  <div className="transcript-content">
                    {episode.transcript.split('\n').map((paragraph, index) => (
                      paragraph.trim() && <p key={index}>{paragraph}</p>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div className="episode-platforms-large">
              <h3>Listen & Subscribe</h3>
              <div className="platform-buttons">
                <a 
                  href={episode.platforms.youtube} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="platform-button youtube"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                  Watch on YouTube
                </a>
                
                <a 
                  href={episode.platforms.spotify} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="platform-button spotify"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
                  </svg>
                  Listen on Spotify
                </a>
                
                <a 
                  href={episode.platforms.apple} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="platform-button apple"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/>
                  </svg>
                  Listen on Apple Podcasts
                </a>
              </div>
            </div>
          </div>
          
          <div className="more-episodes">
            <h3>More Episodes</h3>
            <div className="related-episodes">
              {episodes
                .filter(ep => ep.id !== episode.id)
                .slice(0, 3)
                .map(ep => (
                  <Link to={`/episodes/${ep.id}`} key={ep.id} className="related-episode">
                    <img src={ep.thumbnail} alt={ep.title} />
                    <div className="related-episode-info">
                      <p className="related-episode-date">
                        {new Date(ep.publishDate).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric', 
                          year: 'numeric' 
                        })}
                      </p>
                      <h4>{ep.title}</h4>
                    </div>
                  </Link>
                ))}
            </div>
            <Link to="/episodes" className="btn-secondary">
              View All Episodes
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Episode;
