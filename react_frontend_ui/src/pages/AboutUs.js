import React from "react";
import "./AboutUs.css";

function AboutUs() {
  return (
    <div className="about-us">
      <div className="header-section">
        <h1>About Us</h1>
        <p>
          Welcome to our comic book search system! We are passionate about
          helping comic book enthusiasts find the books they love. We understand
          the challenges of finding the perfect book. We've created a search
          engine that takes into account not only genre and theme, but also more
          nuanced factors such as story pace and comic book cover art. We
          believe that every comic book reader has unique tastes, and our system
          is designed to help personalize the search experience for each user.
          User acts as co-pilot of the system and can take over the
          personalization from the system to tune it as they like. We also
          attempt to provide you with answers on "Why did i get these search
          results?" through local and global explanations. We welcome feedback
          from our users and are always open to suggestions for how we can
          better serve the comic book community. Thank you for using our search
          system and we hope you find your next favorite comic book!
        </p>
      </div>
      <div className="systems-section">
        <h2>Search Systems</h2>
        <p>Choose a system from the navbar dropdown. Each variant is designed to test different aspects of adaptive and explainable search.</p>
        <div className="systems-table-wrapper">
          <table className="systems-table">
            <thead>
              <tr>
                <th>System</th>
                <th>Coarse Search (200 books)</th>
                <th>Domain Facets (20 books)</th>
                <th>Global Explanation</th>
                <th>Reranking</th>
                <th>Comparison Explanation</th>
                <th>Personalization Explanation</th>
                <th>Free-Text Search</th>
                <th>Best For</th>
              </tr>
            </thead>
            <tbody>
              <tr className="row-recommended">
                <td><strong>Wayne ⭐</strong></td>
                <td>TF-IDF, CLD, EHD, HOG</td>
                <td>✅ Adaptive</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>General use (recommended)</td>
              </tr>
              <tr>
                <td><strong>Stark</strong></td>
                <td>TF-IDF, CLD, EHD, HOG</td>
                <td>✅ Adaptive</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>⚠️ Random</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>Testing comparison explanation quality RQ4</td>
              </tr>
              <tr>
                <td><strong>Croft</strong></td>
                <td>TF-IDF, CLD, EHD, HOG</td>
                <td>✅ Adaptive</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>🎲 Random</td>
                <td>✅ via BM25</td>
                <td>Testing personalization explanation quality RQ3</td>
              </tr>
              <tr>
                <td><strong>Butcher</strong></td>
                <td>TF-IDF, CLD, EHD, HOG (top 20 direct)</td>
                <td>❌ No</td>
                <td>🎲 Random</td>
                <td>❌ No</td>
                <td>✅ Yes</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>Baseline (no personalization) RQ2</td>
              </tr>
              <tr>
                <td><strong>Gray</strong></td>
                <td>🎲 Random</td>
                <td>🎲 Random</td>
                <td>🎲 Random</td>
                <td>🎲 Random</td>
                <td>✅ Yes</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>Random control for personalization RQ1</td>
              </tr>
              <tr className="row-bm25">
                <td><strong>BM25 (Not Evaluated)</strong></td>
                <td>BM25</td>
                <td>❌ No</td>
                <td>🎲 Random</td>
                <td>❌ No</td>
                <td>✅ Yes</td>
                <td>🎲 Random</td>
                <td>✅ Native</td>
                <td>Keyword / free-text search <b><i>(Added 2026-04-11)</i></b></td>
              </tr>
              <tr className="row-bm25-wayne">
                <td><strong>BM25_Wayne</strong></td>
                <td>BM25, CLD, EHD, HOG</td>
                <td>✅ Adaptive</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Yes</td>
                <td>✅ Intelligent</td>
                <td>✅ via BM25</td>
                <td>BM25 based Wayne  <b><i>(Added 2026-04-17)</i></b></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="systems-note">
          💡 <strong>Tip:</strong> All systems accept free-text queries (e.g. "batman detective crime") — results are powered by BM25 ranking with all feature weights set to 1.0.
        </p>
      </div>
      <div className="video-section">
        <iframe
          width="560"
          height="315"
          src="https://www.youtube.com/embed/v-ayZLISUOw" //https://youtu.be/v-ayZLISUOw
          title="Book Search Project Video"
          frameBorder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        ></iframe>
      </div>
      <div className="contact-section">
        <h2>Contact Us</h2>
        <ul>
          <li>Email: suraj110693ag@gmail.com</li>
          <li>Phone: 123-456-7890</li>
          <li>Address: Ovgu, Magdeburg</li>
        </ul>
      </div>
      <div className="form-section">
        <h2>Submit Your Feedback</h2>
        <p>
          Have a suggestion or found a bug? Let us know by filling out our
          feedback form.
        </p>
        <a
          href="https://forms.gle/CpH5m8a6sJFpHFEd9"
          target="_blank"
          rel="noopener noreferrer"
          className="google-form-button"
        >
          Submit Feedback
        </a>
      </div>
    </div>
  );
}

export default AboutUs;
