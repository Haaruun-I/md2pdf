{ pkgs ? import <nixpkgs> {} }:

pkgs.python3Packages.buildPythonApplication {
  pname = "md2pdf";
  version = "1.0.0";

  src = ./.;

  propagatedBuildInputs = with pkgs.python3Packages; [
    playwright
    markdown-it-py
    linkify-it-py
    pygments
  ] ++ [ 
    pkgs.playwright-driver.browsers
    pkgs.nodejs_22
  ];

  nativeBuildInputs = [ pkgs.makeWrapper pkgs.nodejs_22];

  postInstall = ''
    wrapProgram $out/bin/md2pdf \
      --set PLAYWRIGHT_BROWSERS_PATH ${pkgs.playwright-driver.browsers} \
      --set PLAYWRIGHT_NODEJS_PATH ${pkgs.nodejs_22}/bin/node \
      --prefix PATH : ${pkgs.nodejs_22}/bin
  '';
  

  meta = {
    description = "";
    license = pkgs.lib.licenses.mit;
    maintainers = with pkgs.lib.maintainers; [ "you" ];
  };
}
