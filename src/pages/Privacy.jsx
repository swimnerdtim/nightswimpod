import './Privacy.css';

function Privacy() {
  return (
    <div className="privacy-page">
      <section className="section">
        <div className="container">
          <div className="privacy-hero">
            <h1 className="section-title">PRIVACY POLICY</h1>
            <p className="privacy-updated">Last updated: August 3, 2026</p>
          </div>

          <div className="privacy-content">
            <p>
              Night Swim Podcast ("we," "us," or "our") operates nightswimpod.com (the "Site"). This
              Privacy Policy explains what information we collect, how we use it, and the choices you
              have when you visit our Site or interact with us.
            </p>

            <h2>Information We Collect</h2>
            <p>
              We collect minimal information through the Site. This may include:
            </p>
            <ul>
              <li>
                <strong>Usage data</strong> — standard analytics such as pages visited, browser type,
                device type, and referring URLs, collected automatically when you browse the Site.
              </li>
              <li>
                <strong>Contact information</strong> — if you sign up for our email list or contact us
                directly, we collect the information you provide (e.g., name, email address).
              </li>
              <li>
                <strong>Cookies</strong> — small data files that may be used to remember preferences and
                understand how visitors use the Site.
              </li>
            </ul>

            <h2>How We Use Information</h2>
            <p>We use the information we collect to:</p>
            <ul>
              <li>Operate, maintain, and improve the Site</li>
              <li>Send episode updates or newsletters to subscribers who opt in</li>
              <li>Understand how visitors use the Site so we can make it better</li>
              <li>Respond to inquiries and communicate with you</li>
            </ul>
            <p>We do not sell your personal information to third parties.</p>

            <h2>Third-Party Services</h2>
            <p>
              The Site links to and embeds content from third-party platforms, including YouTube,
              Spotify, Apple Podcasts, Instagram, TikTok, and Facebook. These platforms have their own
              privacy policies governing any data they collect, and we encourage you to review them.
              We are not responsible for the privacy practices of these third-party sites.
            </p>

            <h2>Analytics</h2>
            <p>
              We may use standard web analytics tools to understand Site traffic and usage patterns.
              These tools may use cookies or similar technologies to collect anonymized or aggregated
              data. You can control cookies through your browser settings.
            </p>

            <h2>Children's Privacy</h2>
            <p>
              The Site is not directed at children under 13, and we do not knowingly collect personal
              information from children under 13.
            </p>

            <h2>Your Choices</h2>
            <p>
              You can opt out of email communications at any time by using the unsubscribe link in any
              email we send, or by contacting us directly. You can also disable cookies through your
              browser settings, though this may affect how the Site functions.
            </p>

            <h2>Changes to This Policy</h2>
            <p>
              We may update this Privacy Policy from time to time. Any changes will be posted on this
              page with an updated "Last updated" date.
            </p>

            <h2>Contact Us</h2>
            <p>
              If you have questions about this Privacy Policy, please contact us through our social
              channels linked in the footer below, or reach out to our presenting partner{' '}
              <a href="https://swimnerd.com" target="_blank" rel="noopener noreferrer" className="host-link">
                Swimnerd
              </a>.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Privacy;
