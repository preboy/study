set nocompatible
runtime macros/matchit.vim
source $VIMRUNTIME/vimrc_example.vim


set diffexpr=MyDiff()
function! MyDiff()
  let opt = '-a --binary '
  if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
  if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
  let arg1 = v:fname_in
  if arg1 =~ ' ' | let arg1 = '"' . arg1 . '"' | endif
  let arg2 = v:fname_new
  if arg2 =~ ' ' | let arg2 = '"' . arg2 . '"' | endif
  let arg3 = v:fname_out
  if arg3 =~ ' ' | let arg3 = '"' . arg3 . '"' | endif
  if $VIMRUNTIME =~ ' '
    if &sh =~ '\<cmd'
      if empty(&shellxquote)
        let l:shxq_sav = ''
        set shellxquote&
      endif
      let cmd = '"' . $VIMRUNTIME . '\diff"'
    else
      let cmd = substitute($VIMRUNTIME, ' ', '" ', '') . '\diff"'
    endif
  else
    let cmd = $VIMRUNTIME . '\diff'
  endif
  silent execute '!' . cmd . ' ' . opt . arg1 . ' ' . arg2 . ' > ' . arg3
  if exists('l:shxq_sav')
    let &shellxquote=l:shxq_sav
  endif
endfunction



" --------------------------------------------------------------
"            Edit by user
" --------------------------------------------------------------


" Change Tab into Space
set expandtab
set tabstop=4
set shiftwidth=4
" set softtabstop=4

set nowrap

set encoding=utf-8              " 如此编译的是Unicode文件出现乱码，可以将这一行打开
" set termencoding              " No usage in Windows/Gvim
set langmenu=en_US
" let $LANG="en_US"             " Not understand
language message en_US          " for English report or tips


set fileencodings=cp936,ucs-bom,utf-8,latin1
set fileencoding=utf-8        " Default file encoding : UTF-8
set fileformats=unix,dos,mac
set fileformat=unix             " Default file format : UNIX

syntax on                       " Open Syntax Highlighting
colorscheme desert              " Syntax Coloring
set nobackup                    " No backup file
set noundofile                  " No undo file
" set guifont=Consolas:h14        " Default font information
" au GUIEnter * simalt ~x         " Maximize window
set number                      " Display line number
set laststatus=2                " Display task bar
set autoindent                  " Smart indenting
" set cursorline                  " Highlight line cursor
set tags=tags;
set autochdir                   " 自动切换到当前编辑的文件目录
set autowrite                   " 自动存档(避免切换操作的时候讨厌的提示)


" Code Complete
filetype plugin indent on
set completeopt=longest,menu

" Be added after the vim upgraded to vim8(H L, zz, ... not correct)
set scrolloff=0


" for search
set ignorecase
set nosmartcase


" self-define map key
nnoremap <C-Tab>    :bn<CR>
nnoremap <C-S-Tab>  :bp<CR>



" --------------------------------------------------------------
"           AutoComplete () {} [] " and '
" --------------------------------------------------------------
" inoremap ( ()<ESC>i
" inoremap ) <c-r>=ClosePair(')')<CR>
" inoremap { {}<ESC>i
" inoremap } <c-r>=ClosePair('}')<CR>
" inoremap [ []<ESC>i
" inoremap ] <c-r>=ClosePair(']')<CR>
" inoremap < <><ESC>i
" inoremap > <c-r>=ClosePair('>')<CR>

" inoremap " ""<ESC>i
" inoremap ' ''<ESC>i
" inoremap ` ``<ESC>i


function! ClosePair(char)
    if getline('.')[col('.') - 1] == a:char
        return "\<Right>"
    else
        return a:char
    endif
endfunction

" switch menu language to English version
source $VIMRUNTIME/delmenu.vim
source $VIMRUNTIME/menu.vim

" change pwd to current buffer files dirctory!
" cd = change dir
nnoremap <Leader>cd :<C-U>cd %:p:h <CR>

" trim tail verbose space on the end line
" ds =  delete space
nnoremap <Leader>ds :<C-U>%s/\s\+$//<CR>

" ad
nnoremap <Leader>e :<C-U>!explorer %:p:h <CR>

" :noh
nnoremap <Leader>a :<C-U>noh<CR>



" insert time
nnoremap <Leader>m A -- by Preboy.ZHANG at <Esc>"=strftime("%c")<CR>p
" inoremap <C-D> -- by Preboy.ZHANG at <C-R>=strftime("%c")<CR>

" 去掉我不想要的map
" unmap <C-Y>


" convenience for modify config file & unhighlight.
map <F4> :noh<CR>

inoremap <C-B> <ESC>ddk$a


" from Mr.Long
nmap <C-j> <C-e>
nmap <C-k> <C-y>

" for vim diff
highlight DiffAdd    cterm=bold  ctermbg=yellow
highlight DiffDelete cterm=bold  ctermbg=cyan
highlight DiffChange cterm=bold  ctermbg=green
highlight DiffText   cterm=bold  ctermbg=red


" for golang support
au BufRead,BufNewFile *.go set filetype=go

" F5 to run this file
nmap <F5> :!./%<CR>
