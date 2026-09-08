import { navigate } from './router.js';

export function Link({ href, children, class: cls, ...rest }) {
  return (
    <a
      href={href}
      class={cls}
      onClick={(e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        navigate(href);
        window.scrollTo(0, 0);
      }}
      {...rest}
    >{children}</a>
  );
}
