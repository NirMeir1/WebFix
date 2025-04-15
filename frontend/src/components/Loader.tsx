export default function Loader() {
    return (
      <div className="flex flex-col items-center justify-center p-6">
        <div className="flex space-x-3 mb-4">
          <span className="w-5 h-5 bg-green-500 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
          <span className="w-5 h-5 bg-green-500 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
          <span className="w-5 h-5 bg-green-500 rounded-full animate-bounce"></span>
        </div>
        <p className="text-lg text-gray-800 font-semibold text-center">
          Running CRO magic on your site, it may take a few seconds...
        </p>
      </div>
    );
  }  