import { useEffect } from 'react';

interface ClarityProps {
  clarityId: string;
}

declare global {
  interface Window {
    clarity: any;
  }
}

const Clarity: React.FC<ClarityProps> = ({ clarityId }) => {
  useEffect(() => {
    (function(c: any, l: any, a: any, r: any, i: any, t?: any, y?: any) {
      c[a] = c[a] || function() { (c[a].q = c[a].q || []).push(arguments) };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", clarityId);
  }, [clarityId]);

  return null;
};

export default Clarity;