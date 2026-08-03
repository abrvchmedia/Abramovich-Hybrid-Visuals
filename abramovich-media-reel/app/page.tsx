export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              Local Streaming Launch — Abramovich Media
            </h1>
            <nav className="hidden md:flex items-center gap-6 text-sm text-gray-600">
              <a href="#" className="hover:text-gray-900">Portfolio</a>
              <a href="#" className="hover:text-gray-900">Case Study</a>
              <a href="#" className="hover:text-gray-900">OTT / CTV</a>
              <a href="#" className="hover:text-gray-900">More Channels</a>
              <a href="#" className="hover:text-gray-900">Calculator</a>
              <a href="#" className="hover:text-gray-900">Offer</a>
              <a href="#" className="hover:text-gray-900">Download PDF</a>
              <a href="#" className="hover:text-gray-900">Print / Save PDF</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <section className="mb-20">
          <div className="text-center mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              DP / Cinematographer Reel
            </h2>
            <h3 className="text-4xl font-bold text-gray-900 mb-6">
              Quality Cinematography for Your Ads on Streaming
            </h3>
            <p className="text-lg text-gray-600 mb-8">
              Elijah Garcia - Cinematographer
            </p>
            <a href="#" className="text-blue-600 hover:text-blue-700 underline">
              Main Portfolio
            </a>
          </div>
        </section>

        {/* Director Reel Section */}
        <section className="mb-20 border-t border-gray-200 pt-12">
          <div className="max-w-4xl">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Jonathan Abramovich — Film & Media Reel
            </h3>
            <p className="text-lg text-gray-700 mb-8">
              Director-led commercial production. Cinema camera systems, on-set leadership, 
              and finished spots built for broadcast and streaming.
            </p>
            <a href="#" className="text-blue-600 hover:text-blue-700 underline font-medium">
              Case Study
            </a>
          </div>
        </section>

        {/* Trattoria Case Study */}
        <section className="mb-20 border-t border-gray-200 pt-12">
          <div className="max-w-4xl">
            <h3 className="text-3xl font-bold text-gray-900 mb-4">
              Trattoria Italia — Las Vegas Restaurant Commercial
            </h3>
            <p className="text-lg text-gray-700 mb-12">
              Luxury restaurant commercial paired with a four-week Connected TV campaign 
              targeting Las Vegas households — cinematic production and premium streaming 
              distribution to maximize local awareness and brand recall.
            </p>

            {/* Campaign Breakdown */}
            <div className="mb-12">
              <h4 className="text-2xl font-bold text-gray-900 mb-8">Campaign Breakdown</h4>
              
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                {/* Client / Market */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Client / Market</h5>
                  <p className="text-gray-700">
                    <strong>Trattoria Italia</strong><br />
                    Las Vegas, NV
                  </p>
                </div>

                {/* Production */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Production</h5>
                  <ul className="text-gray-700 space-y-1">
                    <li>1-day commercial shoot</li>
                    <li>14-person film crew</li>
                    <li>ARRI Alexa Mini cinema package</li>
                  </ul>
                </div>

                {/* Advertising Budget */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Advertising Budget</h5>
                  <p className="text-gray-700">
                    <strong className="text-2xl">$20,000</strong><br />
                    Connected TV (CTV)<br />
                    Las Vegas ZIP code targeting
                  </p>
                </div>

                {/* Estimated Reach */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Estimated Reach</h5>
                  <ul className="text-gray-700 space-y-1">
                    <li>~470,000 impressions</li>
                    <li>~432,000 completed views</li>
                  </ul>
                </div>

                {/* Average CPM */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Average CPM</h5>
                  <p className="text-gray-700">
                    <strong className="text-2xl">$42.50</strong><br />
                    Cost per 1,000 impressions
                  </p>
                </div>

                {/* Campaign Length */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h5 className="font-semibold text-gray-900 mb-3">Campaign Length</h5>
                  <p className="text-gray-700">
                    <strong className="text-2xl">4 weeks</strong><br />
                    Premium streaming TV campaign
                  </p>
                </div>
              </div>

              {/* Target Audience */}
              <div className="bg-gray-50 p-6 rounded-lg mb-8">
                <h5 className="font-semibold text-gray-900 mb-3">Target Audience</h5>
                <p className="text-gray-700">
                  <strong>Adults 30–65</strong><br />
                  Las Vegas residents<br />
                  Fine dining · luxury lifestyle · entertainment
                </p>
              </div>

              {/* Streaming Distribution */}
              <div className="bg-gray-50 p-6 rounded-lg mb-8">
                <h5 className="font-semibold text-gray-900 mb-3">Streaming Distribution</h5>
                <p className="text-gray-700">
                  Disney+, Hulu, Paramount+, Peacock, Roku, Tubi, Prime Video, 
                  premium connected TV inventory
                </p>
              </div>
            </div>

            {/* Estimated Results */}
            <div className="bg-blue-50 border-l-4 border-blue-600 p-8 mb-8">
              <h5 className="text-xl font-bold text-gray-900 mb-4">Estimated Results</h5>
              <ul className="space-y-2 text-gray-700">
                <li>• ~470,000 targeted impressions</li>
                <li>• ~432,000 completed video views (92% VCR)</li>
                <li>• Estimated cost per completed view: $0.046</li>
                <li>• Geographic targeting throughout Las Vegas</li>
                <li>• Premium streaming TV placement</li>
                <li>• Campaign optimized during the 4-week flight</li>
              </ul>
            </div>

            {/* Executive Summary */}
            <div className="mb-8">
              <h5 className="text-xl font-bold text-gray-900 mb-4">Executive Summary</h5>
              <p className="text-gray-700 mb-4">
                Abramovich Media produced a luxury restaurant commercial and planned a 
                four-week Connected TV campaign targeting Las Vegas households. The campaign 
                combines cinematic production with premium streaming TV distribution to 
                maximize local awareness and brand recall.
              </p>
              <p className="text-sm text-gray-600 italic">
                Disclaimer: Campaign metrics shown are planning estimates for proposal 
                purposes and will vary based on inventory availability, targeting, 
                seasonality, and final media-buying performance.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-600 text-sm">
            © {new Date().getFullYear()} Abramovich Media. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
