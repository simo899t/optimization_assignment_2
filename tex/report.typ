#import "temp/temp.typ": *

// ─── Settings ────────────────────────────────────────────────────────────────
#let courseid   = "AI505"
#let coursename = "Optimization"
#let term       = "Spring 2026"
#let dept       = "Department of Mathematics and Computer Science"
#let university = "University of Southern Denmark, Odense"
#let authors    = "Simon Holm, Johannes Rothe"
#let assnr      = "2"
#show: code-style
// ─── Page layout ─────────────────────────────────────────────────────────────
#set page(
  paper: "a4",
  margin: 2.7cm,
  header: context {
    set text(size: 10pt)
    if counter(page).get().first() == 1 {
      grid(
        columns: (1fr, auto),
        align: (left + horizon, right + horizon),
        [#dept \ #university],
        [29 May 2026 \ #authors],
      )
      v(-6pt)
      line(length: 100%, stroke: 0.4pt)
    } else {
      align(right)[#authors]
      v(-6pt)
      line(length: 100%, stroke: 0.4pt)
    }
  },
  footer: context {
    line(length: 100%, stroke: 0.4pt)
    v(-6pt)
    align(center)[
      #set text(size: 10pt)
      Page #counter(page).display() of #counter(page).final().first()
    ]
  },
)
// STIX Two Math
// OldStandard-Math
// ─── Typography ───────────────────────────────────────────────────────────────
#show math.equation: set text(font: "New Computer Modern Math")
#set text(font: "New Computer Modern", size: 12pt)
#set par(justify:true,leading: 0.65em, spacing: 2em, first-line-indent: 0pt)
#show figure.where(kind: raw): set figure(supplement: [Code snippet]) // <- sæt til whatever
// Number equations
#set math.equation(numbering: "(1)")
#let lb = $l b$
// Section numbering
//#set heading(numbering: "1.1")

// ─── Algorithm block helper ───────────────────────────────────────────────────
#let algorithm(caption: none, body) = {
  set text(size: 10pt)
  block(
    width: 100%,
    stroke: (top: 1pt, bottom: 1pt),
    inset: (x: 8pt, y: 6pt),
  )[
    #if caption != none [
      *Algorithm:* #caption \
      #line(length: 100%, stroke: 0.4pt)
      #v(-16pt)
    ]
    #body
  ]
}

// ─── Title ────────────────────────────────────────────────────────────────────
#v(-4pt)
#align(left)[
  #text(size: 11pt)[#courseid -- #coursename]
  #v(0.2cm)
  #text(size: 14pt, weight: "bold")[
    Answers to Obligatory Assignment #assnr, Spring 2026
  ]
  #v(0.4em)
  #line(length: 100%, stroke: 0.8pt)
]
#pagebreak()
#outline()
// ─── Case 1 ───────────────────────────────────────────────────────────────────
#pagebreak()
#set math.mat(delim: "[")
= Case 1
Let $ P = {x in RR^n | tran(bold(a)_i) x <= b_i, i = 1, dots, m  } $
be a nonempty, bounded polyhedron with nonempty interior.

== Task 1 - Defining the center
The center $x^* in P$ is defined by creating barrier functions that penalize by getting close the "sides" of the polyhedron, and then minimizing over $bold(x)$:
This is done by rewriting the linear constraint $tran(bold(a))_i bold(x) <= b_i$ to $s_i = tran(bold(a))_i bold(x)- b_i$ such that the variable $s_i$ describes the slack, or distance to the barrier. This can be made into a function whose output is the $bold(x)$ "closeness" to violating each constraint: 
$ g_i (bold(x))&=tran(bold(a))_i bold(x) - b_i    $
This is then turned into a log barrier, such that the closer the point is to the constraint, the penalty gets exponentially larger, allowing for a complete unconstrained problem:

$ min_(bold(x)in RR^n) f(bold(&x)) quad  \
 f(bold(&x))= -sum_(i=1)^m log(-g_i (bold(x)) )
\ g_i (bold(&x))=tran(bold(a))_i bold(x) - b_i   
$
This minimization satisfies all the given criterium of:
 + It lies strictly within $P$, since the closer the inner term gets to zero, (i.e the slack value decreases) the penalty explodes towards infinity because of the log barrier, and at last becomes undefined at $0^+$. The domain of the function therefore needs to be:
 $ bold(x) in D quad D={bold(x) in RR^n : g_i (bold(x)) < 0 "for " i=1,...,m} $
 + It favors all the constraints equally (none are controlled with a constant) and the minimizing of $bold(x)$ will find the point that minimizes _all_ the constraints, i.e. gets as far away from all the sides as possible, ending in the middle of the polyhedron.
 + The log function is continuos on its domain. 





#pagebreak()
== Task 2 - Analytical properties

=== Computing the gradiens and the hessian

To compute $nabla f(bold(x))$, the function $f(bold(x))= - sum_i log(-g_i (bold(x)))$ will be differentiated using the chain rule. Since the sum element of the function can just be viewed as a repeated application of the sum rule, differentiating the term in the sum, replaces all terms in the sum. The $log(-g_i (bold(x)))$ term can be differentiated with the chain rule:
$ 
phi(bold(x))&= -g_i (bold(x)) = -(tran(bold(a))_i bold(x) -b_i ) \ 
z &= phi(bold(x))\
sigma(z)&= log(z)  \
(partial ) / (partial bold(x)) phi(bold(x))&= - bold(a)_i \
ddz sigma(z)&=  1/z \
(partial) / (partial bold(x)) sigma(phi(bold(x)))&= ( - bold(a)_i ) / (-(tran(bold(a))_i bold(x) -b_i  )) = (  bold(a)_i ) / ((tran(bold(a))_i bold(x) -b_i  ))=   bold(a)_i (tran(bold(a))_i bold(x) - b_i )^(-1) \
nabla f(bold(x)) &= - msum  bold(a)_i (tran(bold(a))_i bold(x) - b_i )^(-1)
$


This describes the gradient of the function $f(bold(x))$, i.e the change for each $x$ value in $bold(x)$. The hessian will then be the change for each $x$, if it is differentiated with either itself, or another $x in bold(x)$:
$ nabla^2f(bold(x))= mat(
  (partial^2f) / (partial x_1^2),  ... , (partial^2f) / (partial x_1 partial x_n); 
  dots.v, dots.down, dots.v;
  (partial^2f) / (partial x_n partial_1), dots, (partial^2f) / (partial x_n^2) 
)
  $


#pagebreak()
Therefore the function can be differentiated again using the chain rule:
$ 
phi(bold(x))&=(tran(bold(a))_i bold(x)-b_i) \
z &= phi(bold(x))\
sigma(z) &= (z)^(-1) \
(partial) / (partial z) sigma(z) &= -1(z)^(-2) quad quad &|" Outer term" \
 (partial) / (partial bold(x)) phi(bold(x)) &= tran(bold(a)_i) quad quad &| " Inner term"\
 (partial) / (partial bold(x))  sigma(phi(bold(x))) &= msum (tran(bold(a))_i )/ (tran(bold(a))_i bold(x)-b_i)^2 \
 &= msum (bold(a)_i tran(bold(a))_i)/ (tran(bold(a))_i bold(x)-b_i)^2 quad quad &|" Multiply the "bold(a_i) "constant"\
$
Meaning:
$ nabla^2f(bold(x)) = msum (bold(a)_i tran(bold(a))_i)/ (tran(bold(a))_i bold(x)-b_i)^2 $

#pagebreak()
=== Proving convexity 

By proving that the function is convex and suitable for second order methods, all the requirements of task 1 will be satisfied.
==== Using affine and convex properties



The function $-msum log(-tran(bold(a)_i) bold(x) -b_i)$ can be split into a sum with non-negative scalar, an inner affine function and an outer convex function. 

$ 
-msum phi_i (bold(x)) &=msum 1 dot (-phi_i (bold(x))) qquad & "Non negative scalar" \ sigma_i (bold(x)) &= -(tran(bold(a))_i bold(x) - b_i) qquad &"Affine"  \ 
   phi_i (bold(x)) &= -log(sigma_i (bold(x))) qquad &"Convex"
  $
 By the following propositions;

#definition(title: [Proposition: Convexity under sums], [
    If ${f_i}_(j in {1,dots,m})$ are convex and $alpha_j_(j in {1,dots,m}) $ is non-negative, then $summ(j=1,m,alpha_j f_j)$ and #h(3em) $max_(j in {1,dots,m}) f_j$  are convex
  ])
#definition(title: [Proposition: Convexity on composition], [
    If $f: RR^d -> RR$ is convex and $A:RR^d -> RR^d$ is affine then $f compose A:RR^d -> RR$ is convex
  ])

  And since $sigma$ is affine, and $log(x)$ is convex, $f(x) = -sum phi$ is also convex.
  This can be seen since the function is a combination of a convex function $log(x)$ (log function are concave, but since the entire function is a sum of these, with a negation in front, they become convex) and affine function $tran(bold(a))_i bold(x) -b_i$.


#pagebreak()
=== Using semi-positive definiteness 

It could also be argued that if the hessian is semi-positive definite that it is convex @Nocedal[p. 30]:
$ nabla^2f(bold(x)) succ.eq 0 quad forall bold(x) in D $
Where $D$ needs to be a convex set. Since the inequality constrains can be defined as half-spaces, the intersections of the half-spaces forms a
convex set as shown on @convex_set.

#figure(
  canvas(length: 1.3cm, {
    import draw: *

    // Extended lines crossing the full canvas
    let s = (paint: luma(140), thickness: 0.5pt, dash: "dashed")
    line((0, 0.5), (5, 0.5), stroke: s)
    line((3.5, 0), (3.5, 3.5), stroke: s)
    line((1, 0), (4.5, 3.5), stroke: s)
    line((4, 0), (0.5, 3.5), stroke: s)
    line((1.5, 0), (1.5, 3.5), stroke: s)

    // Concave polygon (black outline, no fill)
    line((1.5, 0.5), (3.5, 0.5), (3.5, 2.5), (2.5, 1.5), (1.5, 2.5),
      close: true, fill: none, stroke: black + 1.2pt)

    // Convex intersection triangle (filled red)
    line((1.5, 0.5), (3.5, 0.5), (2.5, 1.5),
      close: true, fill: red.lighten(40%), stroke: red.darken(10%) + 1.5pt)
  }),
  caption: [For any concave polygon (black) with infinite lines (half planes). Half-plane intersection (red) is always convex.]
)<convex_set>

The rest can be found by looking at the hessian, and proving that all the entries have to be positive. A matrix is semi-positive definite if it is square and symmetric (which the hessian is by definition) and:
$ tran(bold(v))A bold(v) geq 0 "for all" bold(v) != 0 $

\ Looking at the hessian:

$ msum (bold(a)_i tran(bold(a))_i) / (tran(bold(a))_i bold(x) -b_i)^2 $
It can be observed that the bottom element is squared, thereby guaranteeing positivity. Therefore this can be rewritten as a constant that is multiplied to the other term:
$  $

$ msum c_i (bold(a)_i tran(bold(a))_i)  $

#pagebreak()
Since $bold(a)_i tran(bold(a))_i in RR^(n times n)$, is a matrix, the positive semi-definite property can be tested:
$ &msum c_i (tran(bold(v))bold(a)_i tran(bold(a))_i bold(v)) \
&msum c_i ((tran(bold(v))bold(a)_i)( tran(bold(a))_i bold(v))) quad "The dot product is symmetric" \

&msum c_i (k_i)^2 geq 0 \
$
Which proves that the function is positive semidefinte, and thereby convex.

=== Minimizer
A local minimizer can be defined as:
#definition(title: [Definition: local minimizer], [ A point $bold(x)^*$ is a _local minimum_ (or is a local minimizer) if there exists a $delta>0$ such that $f(bold(x)^*) leq f(bold(x))$ for all $bold(x)$ with $||bold(x)-bold(x)^*||<delta$.
  ])
Which means that for a specific point $bold(x)^* $within a region, $f(bold(x)^*)$ is smaller than all other $f(bold(x))$. This can be argued trough an understanding of the properties of the function. First, the function is continuos and convex, meaning it's overall shape is that of a ball. The domain is strictly bounded within this "bowl", and the function value goes to infinity as the point moves closer to the edge of the "bowl". It can be further argued that this is a global minimizer, not only from the "bowl" analogy, but trough properties. If the previous proposition of a local minimizer is accepted, the following definition:

#definition(title: [Definition: Local Minimizers in Convex Function], [ Assume that $f :RR^n to RR$ is convex, then $bold(x)^*$ is a global minimizer of $f$ if and only if it is a local minimizer. If in addition $f$ is differentiable, then $bold(x^*)$ is a global minimizer of $f$ if and only if it is a stationary point of $f$, ie., $nabla f(bold(x^*))=0$
  ])
Using this property, any local minimizer of a convex function, is a global minimizer.


#pagebreak()
== Task 3

=== Task 3.1
Task 3.1 will first be solved explicitly, and thereafter a python program will be constructed to solve the problem iteratively. The problem can be formulated:


$ f(bold(x)) = - sum_i^5 log(-g_i (bold(&x))) \ 
"Where" g_i (bold(&x)): \

 g_1 (bold(&x)) = 1x_1 + 0x_2 - 1 \
g_2 (bold(&x)) = 0x_1 + 1x_2 - 1 \
g_3 (bold(&x)) = (-1)x_1 + 0x_2 - 1 \
g_4 (bold(&x)) = 0x_1  -1x_2 - 1 \
g_5 (bold(&x)) = 1x_1 + 1x_2 - 1.5 \
$

The Newton method for multivariate functions can be described in updates:
$ bold(x)_(i+1) = bold(x)_i - (nabla^2f (bold(x)_i))^(-1) nabla f(bold(x)_i) $

Here, one stop will be done manually, and then rest of the iterative steps will be done using a python program. First, the hessian and inverse of the hessian can be calculated:

$ sum_i (bold(a)_i tran(bold(a))_i)/ (tran(bold(a))_i bold(x)-b_i)^2 \

( vec(1,0, delim:"[") dot mat(1,0, delim:"[") ) / (mat(1,0, delim:"[") dot vec(0, 0, delim: "[")-1)^2 
=  mat(delim:"[", 1,0;0,0) dot (1) / (-1)^2 = mat(delim: "[", 1, 0; 0, 0)

\

( vec(0,1, delim:"[") dot mat(0,1, delim:"[") ) / (mat(0,1, delim:"[") dot vec(0, 0, delim: "[")-1)^2 
=  mat(delim:"[", 0,0;0,1) dot (1) / (-1)^2 = mat(delim: "[", 0, 0; 0, 1)

\

( vec(-1,0, delim:"[") dot mat(-1,0, delim:"[") ) / (mat(-1,0, delim:"[") dot vec(0, 0, delim: "[")-1)^2 
=  mat(delim:"[", 1,0;0,0) dot (1) / (-1)^2 = mat(delim: "[", 1, 0; 0, 0)

\

( vec(0,-1, delim:"[") dot mat(0,-1, delim:"[") ) / (mat(0,-1, delim:"[") dot vec(0, 0, delim: "[")-1)^2 
=  mat(delim:"[", 0,0;0,1) dot (1) / (-1)^2 = mat(delim: "[", 0, 0; 0, 1)

\

( vec(1,1, delim:"[") dot mat(1,1, delim:"[") ) / (mat(1,1, delim:"[") dot vec(0, 0, delim: "[")-1.5)^2 
=  mat(delim:"[", 1,1;1,1) dot (1) / (-1.5)^2 = mat(delim: "[", (1)/(-1.5)^2, (1)/(-1.5)^2; (1)/(-1.5)^2, (1)/(-1.5)^2)

\
mat(delim: "[", 1, 0; 0, 0) + mat(delim: "[", 0, 0; 0, 1) + mat(delim: "[", 1, 0; 0, 0) + mat(delim: "[", 0, 0; 0, 1) +mat(delim: "[", (1)/(-1.5)^2, (1)/(-1.5)^2; (1)/(-1.5)^2, (1)/(-1.5)^2)   = mat(delim:"[", 2.44, 0.44; 0.44, 2.44)
\
(nabla^2f)^(-1)= (1)/((2.44 dot 2.44) - (0.44 dot 0.44)) mat(delim: "[", 2.44, -0.44; -0.44, 2.44) =  mat(delim: "[", 0.41, -0.07; -0.07, 0.41)
$

And the gradient:
$ - msum (  bold(a)_i ) / ((tran(bold(a))_i bold(x) -b_i  )) \
-( 
vec(delim: "[", -1, 0) +
vec(delim: "[", 0, -1) +
vec(delim: "[", 1, 0) +
vec(delim: "[", 0, 1) +
vec(delim: "[", -0.67, -0.67) 
) = vec(delim: "[", 0.67, 0.67) 
$
And then the newton step:
$
bold(x)_("new") = vec(delim: "[", 0, 0) - mat(delim: "[", 0.41, -0.07; -0.07, 0.41)  dot vec(delim: "[", 0.67, 0.67) = vec(delim: "[", -0.23, -0.23)
$

#pagebreak()
The slack for this point would be:
$ 

g_1 (bold(&x)) = 1x_1 + 0x_2 - 1 = (-0.23) - 1 = -1.23  \
g_2 (bold(&x)) = 0x_1 + 1x_2 - 1 = (-0.23) - 1 = -1.23  \
g_3 (bold(&x)) = (-1)x_1 + 0x_2 - 1 = 0.23 - 1 = -0.77 \
g_4 (bold(&x)) = 0x_1 + (-1)x_2 - 1 = 0.23 - 1 = -0.77 \
g_5 (bold(&x)) = 1x_1 + 1x_2 - 1.5 = (-0.23) + (-0.23) - 1.5 = -1.96\


$
Since the slack is the distance to each barrier, to get the minimum slack, the absolute value of the smallest value is the minimum slack:

$ abs(-0.77)= 0.77
$

#pagebreak()
This can also be expressed in code (@obj_func1), using autograd to compute the gradient and hessian:

#figure(
  ```py
def obj_func(x, order=1):
    def f(x):
        return -(
            anp.log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * 1 + x[1] * 1 - 1.5) )  
            )

    def slack(x):
        return anp.array(
            [(x[0] * 1 + x[1] * 0 - 1),
            (x[0] * 0 + x[1] * 1 - 1),
            (x[0] * (-1) + x[1] * 0 - 1),
            (x[0] * 0 - x[1] * 1 - 1), 
            (x[0] * 1 + x[1] * 1 - 1.5)]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)
```,caption: [The objective function defining both the objective and an array of the slacks of each inequality constraints. It return the slack $s(x)$, the gradient $nf$ and the hessian $nabla^2f$]
)<obj_func1>

That one can then use the newton method as shown on @one_step:

#figure(
  ```py
def newton_method(x):
    _, _, grad, hes = obj_func(x, order=2)
    return x - anp.linalg.inv(hes) @ grad
```, caption: [One step of the newton method]
)<one_step>

#pagebreak()
Using this to test the point $bold(x)= vec(delim: "[", 0,0)$ yields:

#figure(
  ```output
Hessian for original x: [[2.44444444 0.44444444]
 [0.44444444 2.44444444]]
New x after newton method: [-0.23076923 -0.23076923]
Obj value for x with newton method: -0.5642792953243507
Slack for x with newton method: [-1.23076923 -1.23076923 -0.76923077 -0.76923077 -1.96153846]
```,caption: [Output after 1 iteration/step of the newton method as implemented on @one_step]
)
Which matches the earlier calculations. The original point in red, and the new point in green can then be visualized (@feasible_reg):
#figure(
  
  image("assets/image4.png"),
  caption: [The feasible region shown in blue, with the original $bold(x)$ (red) and updated $bold(x)$ (green)]
)<feasible_reg>
But since just doing one iteration is not guaranteed to be the center point, the newton method can be modified to incorporate stopping criterions, such as max iterations or $|f(bold(x_(i+1))) - f(bold(x_i)) |< delta $:
#figure(
  image("assets/newton_algorithm.png", width: 20em),
  caption: [The Newton Method algorithm in pseudocode]
)<newt_psudo>
#figure(
  ```py
def newton_method_stop(x, crit, max_iter):
    i = 0
    while i < max_iter :
        _, _, grad, hes = obj_func(x, order=2)
        x_new = x - anp.linalg.inv(hes) @ grad
        if math.dist(x_new, x) <= crit:
            return x_new
        else:
            x = x_new
        i += 1
    return x
```,caption: [Newton method implemented as from @newt_psudo]
)<newt_impl>
Running this (@newt_impl) with `max_iter=200` and `crit=0.001` yields:
#figure(
  ```output
New x after newton method with stop: [-0.23851648 -0.23851648]
Obj value for x with newton method with stop: -0.5644522715736566
Slack for x after newton method with stop: [-1.23851648 -1.23851648 -0.
76148352 -0.76148352 -1.97703296]

Distance from x after first itertaion, to after full newton method: 0.01095626629433487
Differece in objective value after first x, to after full newton method: 0.0001729762493059006

```, caption: [Output after the iterated newton method (@newt_impl)]
)
#pagebreak()
Here the center point is found to be
$ bold(x)^*=#[`[-0.23851648 -0.23851648]`] $ 
with the minimum slack being = $ abs(-0.76148352) = 0.76148352. $
This can then be visualized aswell:

#figure(
  image("assets/x_newton_with_stop.png", width : 20em),
  caption: [Visualization of the new center after iterative Newton Method \ (@newt_impl)]
)<visual_newt>
And zoomed in:
#figure(
  
  image("assets/zoomed_in.png"),
  caption: [Zooming closer to the new center-point from @visual_newt]
)

#pagebreak()
=== Task 3.2

The change imposed on the last constraint can be expressed as:
$ f(bold(x)) &= (- sum_i^4 log(-g_i (bold(x)))) -log(-(gam tran(bold(a))_5 bold(x) - gam 1.5))\ 
&= (- sum_i^4 log(-g_i (bold(x)))) -(log(gam) + log(-(tran(bold(a))_5 bold(x) - 1.5)))\ quad quad 
$
And since $log(gam)$ is a constant, it disappears when we take the derivative, leaving the feasible and solution set unchanged. This holds for all values of $gam$. The actual value of the objective function does change, since the $gam$ values are still used in calculating them.

The code can be easily modified to take the $gam$ into account by modifying the objective function:
#codly(highlights: (
  (line: 8, start: 31, end: 37, fill: red),
  (line: 8, start: 48, end: 54, fill: red),
  (line: 9, start: 24, end: 32, fill: red),
  (line: 17, start: 22, end: 28, fill: red),
  (line: 17, start: 39, end: 45, fill: red),
  (line: 17, start: 49, end: 57, fill: red)
))
#figure(
  ```py
def obj_func_modified(x, order=1, gam=1):
    def f(x):
        return -(
            anp.log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (1*gam) + x[1] * (1*gam) 
                     - (1.5*gam)))  
            )
    def slack(x):
        return anp.array(
            [-(x[0] * 1 + x[1] * 0 - 1),
            -(x[0] * 0 + x[1] * 1 - 1),
            -(x[0] * (-1) + x[1] * 0 - 1),
            -(x[0] * 0 - x[1] * 1 - 1), 
            -(x[0] * (1*gam) + x[1] * (1*gam) - (1.5*gam))]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)
```,caption: [Objective function, with gamme highlighted in $redmath(#[red])$]
)
And executing this with $gam=10$ yields:
#figure(
  ```output
x with gam=10: [-0.23851648 -0.23851648]
Obj value for x with gam=10: -0.5644522715736567
Slack for x with gam=10: [-1.23851648 -1.23851648 -0.76148352 -0.76148352 -1.97703296]
Distance from x after first itertaion, to after full newton method: 7.850462293418876e-17
Differece in objective value after first x, to after full newton method: -1.1102230246251565e-16
```,caption: [Output after the iterated newton method with gamma modification. (@newt_impl)]
)
Showing that the 2 points are identical (the only difference is computing noise python). This can also be visualized:

#figure(
  image("assets/gam10.png"),
  caption: [Newton method with $gam=10$, the red dot being the starting point, green is after the newton method with no $gam$ and blue $times$ being the newton method with $gam=10$.]
)
#pagebreak()
And zooming in (a lot) does not change that they overlap:
#figure(
  image("assets/gam10_zoomed.png"),
  caption: [Newton method with $gam=10$, green is after the newton method with no $gam$ and blue $times$ being the newton method with $gam=10$.]
)

This can then be done for all the given $gam$ values, yielding the visualization:
#figure(
  image("assets/all_gamgam.png"),
  caption: [Visualization of different $gam$ values.]
)
#pagebreak()
This had the following output:
#figure(
  ```output
  --- Results for gam=0.1 ---
x with gam=0.1: [-0.23851648 -0.23851648]
Obj value for x with gam=0.1: 1.7381328214203888
Distance to x_newton_stop: 7.850462293418876e-17
Difference in objective value from x_newton_stop: 2.3025850929940455

--- Results for gam=1 ---
x with gam=1: [-0.23851648 -0.23851648]
Obj value for x with gam=1: -0.5644522715736566
Distance to x_newton_stop: 0.0
Difference in objective value from x_newton_stop: 0.0

--- Results for gam=10 ---
x with gam=10: [-0.23851648 -0.23851648]
Obj value for x with gam=10: -2.8670373645677025
Distance to x_newton_stop: 7.850462293418876e-17
Difference in objective value from x_newton_stop: -2.302585092994046

--- Results for gam=100 ---
x with gam=100: [-0.23851648 -0.23851648]
Obj value for x with gam=100: -5.169622457561748
Distance to x_newton_stop: 3.925231146709438e-17
Difference in objective value from x_newton_stop: -4.605170185988092

```,caption: [Output after the iterated newton method with gamma modification, using different $gam$ values. (@newt_impl)]
)
#pagebreak()
=== Task 3.3
Normalizing the last constraint is as simple as modifying the code:
#codly(highlights: (
  (line: 8, start: 59, end: 59, fill: red),
  (line: 16, start: 40, end: 40, fill: red),
))
#figure(
  ```py
def obj_func_normalized(x, order=1, gam=1):
    def f(x):
        return -(
            anp.log( -(x[0] * 1 + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 + x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (-1) + x[1] * 0 - 1) ) + 
            anp.log( -(x[0] * 0 - x[1] * 1 - 1) ) + 
            anp.log( -(x[0] * (1*gam) + x[1] * (1*gam) - (1*gam)) )  
            )
    def slack(x):
        return anp.array(
            [-(x[0] * 1 + x[1] * 0 - 1),
            -(x[0] * 0 + x[1] * 1 - 1),
            -(x[0] * (-1) + x[1] * 0 - 1),
            -(x[0] * 0 - x[1] * 1 - 1), 
            -(x[0] * (gam*1) + x[1] * (1*gam) - 1)]
        )

    match order:
        case 0:
            return slack(x), f(x)
        case 1:
            return slack(x), f(x), grad(f)(x)
        case 2:
            return slack(x), f(x), grad(f)(x), jacobian(grad(f))(x)
```,caption: [Objective function, with modifications highlighted in $redmath(#[red])$]
)
#pagebreak()
Where the difference in points can be recompupted:
#figure(
  ```output
--- Results for norm ---
x with norm: [-0.28989802 -0.28989802]
Obj value for x with norm: -0.5567027826682145
Slack for x with norm: [-1.28989802 -1.28989802 -0.71010198 -0.71010198 -2.07979604]
Distance to x_newton_stop: 0.07266446749572646
Difference in objective value from x_newton_stop: 0.007749488905442137
```,caption: [Output of iterative newton method with normalized constraint.]
)

And plotted:
#figure(
  image("assets/norm.png"),
  caption: [The modified feasible space, showing the red initial point, green point for newton method without modified constrains and the blue point for the modified constraint]
)

Here the constraint has been moved, "cutting" a corner of the feasible space out. As the optimization algorithm finds the center of a given feasible space, it will move the center away from the area where the cutout is. This can also be explained as the optimization algorithm tries to balance the distance to each side of the feasible space, and if one of them moves closer, the point should then move accordingly.

#pagebreak()
== Task 4
The problem can be formulated as follows:


Let $ P = {bold(x) in RR^n | tran(bold(a)_i) bold(x) <= b_i, -1 leq x_j leq 1, i = 1, dots, m, j=1 , dots , n  } $

$ f(bold(x))= -msum  log(-(tran(bold(a))_i bold(x) - b_i   ) )
 + sum_(j=1)^n (-log(x_j+1)) + sum_(j=1)^n (-log(1-x_j))
$




By using the standard log barrier on the indivudal values of the vector $bold(x)$, it is possibe make it into an unconstrained linear optimization problem (assuming that the initial point $bold(x) in D$, where $D$ is the convex set). 

By reusing the log barrier properties, each optimization problem of this form will simply treat the $|x_i| leq 1$ as linear constraints.
=== Compute $nabla f(bold(x))$ and $nabla^2 f(bold(x))$
The first term has been found from task 2, the second and third term can be found using the chain rule:
$ 
sum_(j=1)^n (-log(x_j+1))
\ ddx [log(x)] = 1/x
\ ddx [x_j+1]= 1
\ ddx[(-log(x_j+1))] = -(1/(x_j+1))
$

$ 
sum_(j=1)^n (-log(1-x_j))
\ ddx [log(x)] = 1/x
\ ddx [1-x_j]= -1
\ ddx[(-log(1-x_j))] = -( (-1)/ (1 - x_j)  ) = sum_(j=1)^n (1/(1 - x_j ))
$



$ nabla f(bold(x)) =- msum  bold(a)_i (tran(bold(a))_i bold(x) - b_i )^(-1) -sum_(j=1)^n ((1)/(x_j+1))
+sum_(j=1)^n ( (1)/(1-x_j))
$

Since the gradient is a vector, its important that the final output should also be a vector. The sums currently evaluate to scalars, to fix this, the appropriate basis vector is multiplied for each sum term. Since the sum term calculates the gradient value, the $e$ basis vector applies it to the correct element of the gradient vector:
$ nabla f(bold(x)) =- msum  bold(a)_i (tran(bold(a))_i bold(x) - b_i )^(-1) 
-sum_(j=1)^n (bold(e_j)/(x_j+1))
+sum_(j=1)^n ( bold(e)_j/(1-x_j))
$

Now to get the hessian, the same logic is applied. The function gets differentiated:

$ ddx [ -(bold(e)_j / (x_j+1 ))]= [-bold(e)_j (x_j+1)^(-1)]= bold(e)_j (x_j+1)^(-2)  $

$ ddx [bold(e)_j/(1-x_j)] = [bold(e)_j (1-x_j)^(-1)]=-bold(e)_j (1-x_j)^(-2) dot (-1) =bold(e)_j (1-x_j)^(-2) $

$ nabla^2 f(bold(x)) = msum ( (bold(a)_i tran(bold(a)_i)) / (tran(bold(a))_i bold(x)-b_i  )^2 ) 
+ sum_(j=1)^n ((bold(e)_j) / (x_j+1)^2)
+ sum_(j=1)^n ( (bold(e)_j) / (x_j-1)^2)
$

Much like before, now the hessian is a matrix, therefore the output should also be a matrix as well. To do this, another basis vector is multiplied for each sum term.

$ nabla^2 f(bold(x)) = msum ( (bold(a)_i tran(bold(a)_i)) / (tran(bold(a))_i bold(x)-b_i  )^2 ) 
+ sum_(j=1)^n ((bold(e)_j tran(bold(e)_j)) / (x_j+1)^2)
+ sum_(j=1)^n ( (bold(e)_j tran(bold(e)_j)) / (x_j-1)^2)
$


Here it can be reused that the first part is a positive matrix, and since the second and third term are sum of a positive integer divided by something squared, they're also positive. The expression can then be seen as $H+D_1+D_2$ where they are all positive, proving that the hessian is positive semi-definite.

#pagebreak()
=== Prove that $f(bold(x))$ is convex on its domain

Expanding on the proof of convexity, it is already clear that the first term is convex. Since the second term $sum_(j=1)^n (-log(x_j +1))$ and third term $sum_(j=1)^n (-log(1 - x_j))$ are convex using the same logic, the new function is just sums of convex functions, and the proposition for convexity under sums still holds: 
#definition(title: [Proposition: Convexity under sums], [
    If ${f_i}_(j in {1,dots,m})$ are convex and $alpha_j_(j in {1,dots,m}) $ is non-negative, then $summ(j=1,m,alpha_j f_j)$ and #h(3em) $max_(j in {1,dots,m}) f_j$  are convex
  ])<convex_sum>

This can also be proved using the property:

$ nabla^2f(bold(x)) succ.eq 0 quad forall bold(x) in D $

From @Nocedal[p. 30], where $D$ again needs to be a convex set. Using the same arguments as before, the inequality constriants can be seen as half spaces, and this makes the domain a convex set. And since it has been established that the $nabla^2f$ is semi-positive definate, it is also convex




  
Lets test this on a case similar to earlier (but in 3 dimensions!). For this one should ensure that the methods should use 
- *Search direction*
This is the negative gradient, that is 
  $ -nf(x) quad "(steepest descent)" $
- *Backtracking line search*
The step size $alpha_k$ is chosen via strong bracketing, which enforces both the Armijo (sufficient decrease) condition:
$ f(bold(x) + alpha bold(d)) <= f(bold(x)) + beta alpha nabla f_bold(d) (bold(x)) $
and the curvature (strong Wolfe) condition:
$ |nabla f_bold(d) (bold(x) + alpha bold(d))| <= sigma |nabla f_bold(d)(bold(x))| $

#pagebreak()
- A *mechanism to ensure feasibility* (iterates remain in domain)

After each step, the iterate is clipped to remain strictly inside the box constraints:
$ bold(x)_(k+1) = "clip"(bold(x)_k + alpha_k bold(d)_k, -1 + epsilon, 1 - epsilon) $
Such that any overshooting stays within $abs(x) <= 1$
- A *stopping criterion* based on optimality measures: i.e., $norm(nf(x))_2 <= eta$. 
When the gradient norm $norm(nf)$ is sufficiently small, the iterate is near a stationary point (local optima)
#figure(
  ```py
if anp.linalg.norm(g) <= eta:
            break
```,caption: [Stopping criterion stopping the search when close to a local optima.]
)

Lets try this out on simple gradient descent problem with only one other inequality constraint.

Lets 
$ A = mat(0,1,1;) "and" b = mat(0) quad x_0 = mat(0., -0.7, 0.7) $
Where $x_0$ is the initial search point.
#figure(
  image("assets/gdsb1.png",width: 25em),
  caption: [Gradient Descent using line search to find a center point given the barriers, \ $x <=1$ and $A x<=b$ from initial point $x_0$.
\ $x_"best" = $ `[ 0.        -0.4519704  0.4519704]`.]
)<gdsb1>

#figure(grid(columns: 2,
  image("assets/alphasgd1.png"),
  image("assets/conv_gd1.png")
),
caption: [_Left_: Alpha returns during line-search gradient descent from @gdsb1. \ _Right_: Convergence of the objective function from gradient descent from @gdsb1]
)

Lets add another inequality constraint

$ A = mat(0,1,-1;1,0,-1) "and" b = mat(0;0) quad x_0 = mat(0., -0.7, 0.7) $
#figure(
  image("assets/gdsb2.png",width: 25em),
  caption: [Gradient Descent using line search to find a center point given the barriers, \ $x <=1$ and $A x<=b$ from initial point $x_0.$ \ $x_"best" = $ `[-0.40824535 -0.40824813  0.61236766]`.]
)<gdsb2>

#figure(grid(columns: 2,
  image("assets/alphasgd2.png"),
  image("assets/conv_gd2.png")
),
caption: [_Left_: Alpha returns during line-search gradient descent from @gdsb2. \ _Right_: Convergence of the objective function from gradient descent from @gdsb2]
)



#pagebreak()
Lets try and apply the newton method. 

Again let
$ A = mat(0,1,1;) "and" b = mat(0) quad x_0 = mat(0., -0.7, 0.7) $

#figure(
  grid(columns: 1,
image("assets/newt3d1.png",width: 30em),

),
caption: [Newton method using line search to find a center point given the barriers, \ $x <=1$ and $A x<=b$ from initial point $x_0$.
\ $x_"best" = $ `[ 0.         -0.44720245  0.44720245]`.]

)<newt1>
#figure(
  grid(columns: 2,
image("assets/newt3dstep1.png"),
image("assets/newt3dconv1.png")

),
caption: [_Left_: Alpha returns during line-search newton method from @newt1. \ _Right_: Convergence of the objective function from newton method from @newt1]
)

#pagebreak()
Now let $ A = mat(0,1,-1;1,0,-1) "and" b = mat(0;0) quad x_0 = mat(0., -0.7, 0.7) $
#figure(
  grid(columns: 1,
image("assets/newt3d2.png",width: 30em),

),
caption: [Newton method using line search to find a center point given the barriers, \ $x <=1$ and $A x<=b$ from initial point $x_0$.
\ $x_"best" = $ `[-0.40683268 -0.4105287   0.6125544 ]`.]
)<newt2>
#figure(
  grid(columns: 2,
image("assets/newt3dconv2.png"),
image("assets/newt3dstep2.png")
),
caption: [_Left_: Alpha returns during line-search newton method from @newt2. \ _Right_: Convergence of the objective function from newton method from @newt2]
)
#pagebreak()

== Discussion
The gradient descent and Newton methods were both applied to the log-barrier problem in three dimensions, under one and two half-space constraints respectively. In both configurations, both methods successfully converged to a feasible center point, with the Gradient descent method converging in fewer iterations. Interestingly the newton method implementation didn't seem to use the line-search. This might be cause it uses the hessian scale the steps. For convex functions, theory would suggest that newtons methods should converge in fewer steps than the gradient descent. This could be due to the clipping mechanic of the code, interfering with the newtons ability to find the center point. Given more time, with this project, this would be researched more in detail, and perhaps modify the line search code to modify the step size to better account for leaving the feasible set.

== Conclusion on case 1
The $log$-barrier is successfully used to define the a feasible center of the convex polyhedron, with the minimize lying strictly within $P$. Convexity of the barrier function was proven both through the composition of convex and affine function, but also through positive definiteness of the Hessian.

Both gradient descent and Newton's method were applied to the problem in two and three dimensions with one and two inequality constraints. Both methods converged reliably to feasible center points. While both implementations gave good results, the gradient descent proved to perform better in terms of iterations, but this is most likely due to an error in the implementation.


// ─── Case 2 ───────────────────────────────────────────────────────────────────
#pagebreak()
= Case 2 <case2>
In this case the objective is to fairly distributes students across teams such that their attributes match the most. As each attribute carry a weight to determine its importance. 

== Task 1
This can be modeled as a Integer Linear Programming (ILP) problem.

Given the objective function
$ sum_(T in cal(T)) sum_(a in A) w(a)z_(T,a) = sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b) $

Then task is to minimize $sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b)$

Lets go over the different constraints for this problem
1. Each student can only be assigned to exactly 1 team
$ sum_(T in cal(T)) x_(s,T) = 1 quad forall s in S $

2. The size of a team is limited to $ell <= |T| <= u$ 
$ ell <= sum_(s in S) x_(s,T) <= u quad forall T in cal(T) $

3. Two student who share a disagreement, must not be on the same team
$ x_(s_1,T) + x_(s_2,T) <= 1 quad forall (s_1,s_2) in D, forall T in cal(T) $



And so one can define the minimization task as the following:

$ min  sum_(T in cal(T)) sum_(a in A)sum_(b in L_a) w(a)y_(T,a,b)\
st #align($

sum_(T in cal(T)) x_s = 1 quad &forall s in S \

ell <= sum_(s in S) x_s <= u quad &forall T in cal(T) \

x_(s_1,T) + x_(s_2,T) <= 1 quad &forall (s_1,s_2) in D, forall T in cal(T)\

x_(s,T), y_(T,a,b) in {0,1} quad &$) $


#pagebreak()
Task 2, 3 and 4 all implement the `ROAR-NET-API`. This allows using highly optimized construction and search functions like `greedy_construction` and `beam_search`. Since `ROAR-NET-API` is an external framework, is expects a problem to implement certain interfaces like: `SupportsLowerBound` or `SupportsApplyMove`. These interfaces define how the framework can interact with the problem without knowing the specific problem details. 

By using `ROAR-NET-API` one can focus on implementing classes for the Problem, Solution, Move, and Neighbourhood, while the framework handles the search process. Because of this the development process is split into 3 tasks.
1. Solution construction (Task 2)
2. Solution improvement (Task 3)
3. Meta-heuristics (Task 4)

== Task 2 - construction
Lets define problem and implement a solution construction, such that the `ROAR-NET-API` can use it. 

This is done by
1. Defining the problem
2. Define the solution
3. Search for valid moves
4. Initialize the problem iteratively with valid moves


The problem needs a class for defining the problem itself.
#figure(
  ```py
class Problem(...):
    def __init__(...):
        self.n_members = n_members
        self.n_teams = n_teams
        self.weights = weights
        self.attributes = attributes
        self.disagreements = disagreements
        self.min_size = min_size
        self.max_size = max_size
```,caption: [Part of the `Problem` implementation which implements how a problem is defined for this optimization task.]
)<problem>
The problem (@problem) should by use of the method ```py from_textIO(cls, f: textIO)``` translate the `instance` to a problem which is readable from the `ROAR-NET-API`.

#pagebreak()
The problem should moreover initialize the both the neighbourhood and lists a list of sets to map disagreements for each student. This is shown on @problem2. This way the algorithm can always see for any student which other students are in disagreements.
#codly(offset-from: <problem>, smart-indent: true)
#figure(
  ```py
        self.disagrees_with: list[set[int]] = [set() for _ in range(n_members)]
        for a, b in disagreements:
            self.disagrees_with[a].add(b)
            self.disagrees_with[b].add(a)
```,caption: [Part of the `Problem` implementation, this part creates the `disagrees_with`]
)<problem2>
After the problem definition, its also important that the solution is defined. The solution should contain: a reference to the problem instance (so the solution can access problem data), a list of assignments, the labels within each team in the solution, the team sizes, and the lower bound. 

#figure(
  ```py
  class Solution(SupportsCopySolution, SupportsLowerBound):
    def __init__(
        self,
        problem: "Problem",
        assignments: list[int],
        team_labels: list[list[dict[int, int]]],
        team_sizes: list[int],
        lb: int,
    ):

    def objective_value(...):
    def lower_bound(...):
    def copy_solution(...):
    def is_feasible(...):
    def __repr__(...):
```,caption: [The `Solution` class defines what a solution should hold such that methods can make assignments through the optimization process.]
)<solution>
The solution class (@solution) also includes a `objective_value` method, a `lower_bound` method, a `copy_solution` method and a `is_feasible` method. These will all be useful later on, since they are used either in testing or for some of the solvers. Now that the problem is well defined, one can create an empty solution. The `empty_solution`  is then just an instance of a solution with empty teams and a lower bound of 0.
#pagebreak()
Now one can represent the problem as a solution (though an empty one) by `print(Problem.from_textIO(file).empty_solution())`

#figure(
  ```output
Solution(
  assignments=[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
  team_labels=[[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]],
  team_sizes=[0, 0, 0],
  lb=0
)
```,caption: [Empty constructed solution given 13 students and 3 teams]
)<empty>

Notice how on @empty, team assignments are labeled as `-1`, meaning that all students are unassigned.

For the improvement task, its smart construct a feasible solution. This solution might be suboptimal, but it might work better for most improvement methods, rather than a unsigned (unfeasible) solution. For this any of the construction algorithms from `roar_net_api.algorithms` may be used. The `AddNeighbourhood` class (@addNeighbour) should therefore create a neighborhood of moves for such an algorithm. 

#figure(
  ```py
class AddNeighbourhood(SupportsMoves[Solution, AddMove]):
    def __init__(self, problem: "Problem", neighbourhoodType=None):
        self.problem = problem
        self.neighbourhoodType = neighbourhoodType

    def moves(...)
```, caption: [The `AddNeighbourhood` keeps track of the problem, and which neighborhood type is being used at runtime. This will be elaborated later on @moves]
)<addNeighbour>



This `moves()` method is only used while *constructing* the initial solution, because of this, the moves available to the construction algorithms provided by the framework should only consider moves for students which are unassigned. The improvement where students are moved comes later.

#pagebreak()
After this, it may be beneficial to select candidate moves using some additional selection criteria. Initially, the construction can be performed by identifying all feasible moves and greedily selecting the best move at each step. Instead of acting as a traditional heuristic that merely prioritizes moves, the approach used here is closer to neighborhood pruning. Rather than exploring the complete set of feasible moves, only a reduced subset of the neighborhood is considered. The excluded moves are those which are believed to have a low likelihood of improving the situation. Note that although these assumptions are not formally provable (as believed by the authors), it might either reduce the  computational time spent constructing by avoiding exploration of moves that are unlikely to be good.

Lets examine four examples of limiting the neighbourhood.

1. Restrict to moves that fill smaller teams. 
2. Restrict to moves that assigns 'most disagreeing' members
3. Hybrid
4. All feasible moves

For testing efficiency, the `AddNeighbourhood` class implements all four, with a match-case IN THE `moves` method shown on @moves.

#codly(highlights: (
  (line: 4, start: 28, end: 55, fill: red, tag: "1"),
  (line: 7, start: 28, end: 64, fill: green, tag: "2"),
  (line: 10, start: 28, end: 53, fill: blue, tag: "3"),
  (line: 13, start: 28, end: 57, fill: purple, tag: "4"),
))
#figure(
  ```py
def moves(self, solution: Solution) -> Iterable[AddMove]:
        match (self.neighbourhoodType):
            case "minFirst":
                yield from self.minFirst(solution)
            
            case "mostDisagreementsFirst":
                yield from self.mostDisagreementsFirst(solution)

            case "hybridMoves":
                yield from self.hybridMoves(solution)

            case "allFeasible":
                yield from self.allFeasible(solution)
```,caption: [The `moves`method, which selects which kind of move filtering to use. \ This is mostly good implantation practice for easier testing.]
)<moves>
#pagebreak()
All move-methods follow a similar structure of: (1) identify which students to be assigned (those who are unassigned), (2) candidate move filtering, (3) add the moves which are feasible.

#figure(
  ```py
        p = self.problem
        unassigned = [s for s, team in enumerate(solution.assignments)
                      if team == -1]
        if not unassigned:
            return # if no un assigned student, early exit
```, caption: [Part of a generic `moves` which explains the common behavior of the moves methods implemented later on. Here all the unassigned student are selected before any filtering.]
)<genMov>

As shown in @genMov Every move in the construction phase needs to only assign students whom are unassigned.
#codly(
offset-from: <genMov>)
#figure(
  ```py

        for s in unassigned:
            for t in candidate_teams:
                if self.is_feasible_add(s, t, solution):
                    yield AddMove(s, t)
```,caption: [Part of a generic `moves` which explains the common behavior of the moves methods implemented later on. Here all the feasible moves for $s in cal(S)_"unassigned"$ and  $T in cal(T)_"candidates"$ are yielded such that they can be applied by a solver.]
)<genMove2>
Furthermore as shown on (@genMove2), for each student, the move should only yield moves which a permitted under the disagreement rule. By searching blocked teams for a student, allows choosing which teams are blocked due to this rule. The it checks if the a move is feasible before yielding it. Lets now discuss the different kinds of move filtering. For the following methods repeating code is commented out since its the same, unless specified.

=== All feasible moves
One could use the `allFeasible` (@allFeasibleMoves) which captures all feasible moves within the constraints of the problem.
#figure(
  ```py
def allFeasible(self, solution: Solution) -> Iterable[AddMove]
    # identification of unassigned students
  
    under_min = [t for t in all_teams if solution.team_sizes[t] < p.min_size]
    if under_min:
            candidate_teams = under_min
        else:
            candidate_teams = [t for t in all_teams if solution.team_sizes[t] < p.max_size]

  # yield all the legal moves
```,caption: [The `allFeasible` method yield all feasible moves to a solver.]
)<allFeasibleMoves>

=== Restrict to smallest teams
#codly()
#figure(
  ```py
def minFirst(self, solution: Solution) -> Iterable[AddMove]
    # identification of unassigned students
  
    smallest = min(solution.team_sizes[t] for t in all_teams)
    candidate_teams = [t for t in all_teams 
                       if solution.team_sizes[t] == smallest]

    # yield all the legal moves
```, caption: [The `minFirst` method filters moves, such that assignments are only made to the teams with the least assignments (smallest teams) with the most disagreements are assigned first.]
)<min>

The `minFirst` (@min) selects the minimum size out of all possible teams. Then selects the candidate teams as any team which is as small as the smallest team. This should create a balance in the team sizes, that ensures that the smallest teams are prioritized and filled first.

=== Restrict to most disagreeing members
In most assignments tasks, it is often wise to assign the more complex pieces first. The same method might be wise to approach this problem with.
#figure(
  ```py
def mostDisagreementsFirst(self, solution: Solution) -> Iterable[AddMove]
    # identification of unassigned students
  
    max_dis = max(len(p.disagrees_with[s])for s in unassigned) 
    unassigned_priority_students = [s for s in unassigned
                                   if len(p.disagrees_with[s]) == max_dis]  
 
    candidate_teams = [t for t in all_teams 
                     if solution.team_sizes[t] < p.max_size]
    

    for s in unassigned_priority_students:
    # yield all the legal moves
```,caption: [The `mostDisagreementsFirst` method filters moves which assigns students with less disagreements, such that students with the most disagreements are assigned first.]
)<dis>

The `mostDisagreementsFirst` (@dis) method counts the maximum number of disagreements for the set of unassigned students. This way it can prioritize those whom enforce more strict requirements for assignments. By only selecting those with the most disagreements first, moves later on will be more feasible.

#pagebreak()
=== Hybrid of restricting heuristics
While `minFirst` and `mostDisagreementsFirst` each offer distinct advantages, a hybrid approach may capture the benefits of both.

#figure(
  ```py
def hybridMoves(self, solution: Solution) -> Iterable[AddMove]
    # identification of unassigned students
  
    smallest = min(solution.team_sizes[t] for t in all_teams)
    candidate_teams = [t for t in all_teams 
                       if solution.team_sizes[t] == smallest]

        if not candidate_teams:
            candidate_teams = [t for t in all_teams
                               if solution.team_sizes[t] < p.max_size]

    max_dis = max(len(p.disagrees_with[s])for s in unassigned)
    unassigned_priority_students = [s for s in unassigned
                                    if len(p.disagrees_with[s]) == max_dis]

    for s in unassigned_priority_students:
    # yield all the legal moves
```,caption: [The `allFeasible` method is a hybrid version of both the `mostDisagreementsFirst` method and the `minFirst` method. Much like `mostDisagreementsFirst` and `minFirst` it too filters the moves for the solver.]
)<hybrid>
The `hybridMoves` (@hybrid) prioritizes both small teams, *and* disagreeing students. However more constraint might not always better as it might limit restrict the ability to explore more beneficial options in the search space.

#pagebreak()
=== Moving and incremation
Up until now, the lower bound has been incremented as
#let where = $quad "where"$
$ Delta lb(s) = f(s) + h(s) where h(s) = 0 $

where $f(s)$ is the  objective contribution of the move i.e. the weighted sum of new labels introduced and $h(s)$ is a heuristic term estimating future cost. Although a heuristic term $h(s)$ could be used to approximate future cost effects, this is not used as the complexity is not really worth it, given the problem difficulty. Instead, the simpler evaluation based solely on $f(s)$ is good enough for the construction process. This in incremented when a move is applied.

#figure(
  ```py
class AddMove(...):
    def __init__(self, student: int, toTeam: int):
        self.s = student
        self.toTeam = toTeam
        
    def apply_move(self, solution: Solution) -> Solution:
        solution.lb += self.lower_bound_increment(solution)
        solution.assignments[self.s] = self.toTeam
        solution.team_sizes[self.toTeam] += 1
        member_labels = solution.problem.attributes[self.s]
        for a, label in enumerate(member_labels):
            counts = solution.team_labels[self.toTeam][a]
            counts[label] = counts.get(label, 0) + 1
        return solution
```,caption: [`AddMove` class and `apply_move` method implementation, which serves to define what move is, and how it should be applied to a given solution]
)<addMove>
Each `addMove` (@addMove:4) should then keep track of its student and the team. It should then apply the move  by assigning the student to the given team and updating that teams labels. 

#pagebreak()
Any move should increment the lower-bound `lb` for the move such that the objective function can be minimized.

#figure(
  ```py
    def lower_bound_increment(self, solution: Solution) -> float:
        p = solution.problem
        labels_count = solution.team_labels[self.toTeam]
        student_labels = p.attributes[self.s]
        incr = 0
        for a, label in enumerate(student_labels):
            if labels_count[a].get(label, 0) == 0:
                incr += p.weights[a]
        return incr
```,caption: [`lower_bound_increment` implementation, which serves to return the increment of the lower-bound given a certain move.]
)<inc>
The increment (@inc) simply counts the weights of the labels that are absent if the move is made. This way one can determine if a move will be good/bad depending on the `lb`.

=== Testing & comparison
Lets test these against each other with larger instances of data (300 students). Since $lb$ values depend on the heuristic used, they are not directly comparable across runs; instead, the objective value (cost) of the constructed solution is used for comparison. For this both the `greedy_search` and the `beam_search` are used. The `greedy_search` algorithm is a greedy construction algorithm which at each iteration picks the best-scoring move available, repeating until no more moves are available. The main drawback of using a greedy algorithm like `greedy_search` is that it only expands one single solution. The `beam_search` is much more sophisticated in that sense, since it expands multiple solutions simultaneously, and keeps the $k$ best ones. This could make it very powerful when there are many different moves like in this problem. 
#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, right, right),
    table.header([*Restricting heuristic* : greedy_search ], [*cost*], [*Time (sec)*]),
    [minFirst],                 [70510], [$apx$ 0.850],
    [mostDisagreementsFirst ],  [73590], [$apx$ 0.536],
    [hybridMoves],              [70960], [$apx$ 0.540],
    [allFeasible],              [68770], [$apx$ 0.997],
    [*Restricting heuristic* : beam_search - initial: random], [*cost*], [*Time (sec)*],
    [minFirst],                 [104670], [$apx$ 0.002],
    [mostDisagreementsFirst ],  [104700], [$apx$ 0.002],
    [hybridMoves],              [105530], [$apx$ 0.002],
    [allFeasible],              [105170], [$apx$ 0.002]
  ),
  caption: [Construction heuristics comparison on 300 students / 60 teams. ]
)<constructiontests>
#pagebreak()
Greedy construction consistently outperforms beam search across all tests (@constructiontests), achieving costs in the 68770–73590 range compared to 104670–105530 for beam search. This is probably explained by the tie-breaking issue: on an empty solution, beam search breaks on ties which is everywhere on an initial empty solution. One can avoid this with a random initialized solution but introduces a poor initial cost that beam search cannot recover from

Lets see how the best constructed solution looks so far without any improvement yet. This example (@const) combines the best results from earlier.
#figure(
  ```output
  Solution(
  Solution(
  assignments=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 5, 12, 13, 14, 14, 15, 16, 17, 4, 18, 19, 20, 21, 22, 23, 24, 25, 26, 7, 27, 17, 28, 29, 30, 6, 31, 32, 33, 22, 11, 0, 34, 32, 35, 17, 27, 36, 7, 14, 5, 7, 33, 30, 0, 15, 34, 16, 28, 12, 35, 37, 0, 38, 22, 38, 23, 37, 8, 39, 40, 41, 42, 38, 43, 11, 44, 39, 45, 42, 25, 46, 23, 23, 9, 8, 47, 45, 48, 15, 36, 31, 2, 9, 45, 49, 25, 47, 25, 43, 12, 49, 44, 27, 19, 28, 4, 45, 38, 13, 50, 20, 13, 25, 50, 48, 51, 52, 18, 46, 53, 1, 54, 55, 48, 45, 56, 31, 8, 1, 56, 41, 40, 24, 10, 35, 30, 26, 47, 35, 34, 1, 57, 55, 9, 48, 30, 19, 16, 17, 44, 15, 49, 51, 3, 7, 54, 41, 21, 46, 6, 9, 26, 46, 55, 29, 34, 13, 32, 26, 30, 21, 46, 12, 6, 36, 10, 12, 40, 35, 18, 5, 11, 58, 52, 40, 37, 39, 52, 51, 15, 24, 59, 57, 2, 29, 52, 3, 54, 20, 55, 49, 11, 51, 18, 14, 16, 18, 33, 58, 58, 6, 53, 42, 22, 50, 57, 3, 41, 24, 27, 5, 17, 26, 19, 50, 56, 4, 55, 59, 53, 29, 44, 47, 27, 34, 54, 8, 39, 4, 44, 43, 33, 33, 31, 59, 20, 59, 32, 50, 36, 53, 28, 54, 42, 38, 49, 32, 48, 10, 21, 22, 37, 58, 43, 2, 31, 57, 47, 59, 43, 14, 39, 51, 53, 20, 28, 42, 40, 57, 52, 56, 0, 2, 56, 41, 10, 1, 3, 13, 21, 36, 19, 37, 24, 29, 23, 16, 58],
  team_labels=[[{0: 5}, {3: 5}, {3: 2, 5: 3}, ..., {7: 1, 4: 1, 1: 1, 2: 1, 0: 1}]],
  team_sizes=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
  cost=cost=68770
)
Execution time: 0.9978528022766113
Is feasible: True
  ```, caption: [This is the best feasible construction solution using the  \ (_note that team_labels has been reduced, because its very long for 300 student_)]
)<const>

#pagebreak()
== Task 3 - improvement
Now its time to implement some solution improvement methods, such that the `ROAR-NET-API` can use it. Since the algorithms are now improving an already constructed solution, they should move students around rather than add the. The goal in improvement is so make moves that minimizes the `objective_value` as mush as possible.

This is done by
3. Search for valid moves
4. Initialize the problem iteratively with valid moves

Improving a solution can be done in several ways. Here, swap moves are used — exchanging two students between teams — as the local search neighbourhood. The solvers, which are to solve given the following methods, should then be presented a set of moves, and the ability to see the objective value increment of each move. See for example the `best_improvement` method from the `ROAR-NET-API`, which does exactly this
#figure(
  ```py
    for move in neigh.moves(solution):
        incr = move.objective_value_increment(solution)
        assert incr is not None
        if incr < 0:
            yield (move, incr)
```,caption: [`ROAR-NET-API` implementation of `best_improvement` which  utilizes the `move.objective_value_increment(solution)` to select moves ]
)


=== Random sampling heuristic
Firstly one can still change the search space, by for example implementing a random moves. This will serve as an option to a possible heuristic based algorithm like SA to explore non-improving moves unpredictably. The following `randomMoves` is implemented in the `SwapNeighbourhood` class, however a method like this will be implemented for all neighbourhood classes.
#figure(
  ```py 
    def random_move(self, solution: Solution) -> SwapMove | None:
        return next(self.random_moves_without_replacement(solution), None)
        
    def random_moves_without_replacement(self, solution: Solution) -> Iterable[SwapMove]:
        p = self.problem
        n = p.n_students
        total = n * n
        
        for idx in sparse_fisher_yates_iter(total):
            s1 = idx // n
            s2 = idx % n
            if s1 >= s2:
                continue
            
            t1, t2 = solution.assignments[s1], solution.assignments[s2]

            if t1 == t2:
                continue
            if self._is_feasible_swap(s1, s2, t1, t2, solution):
                yield SwapMove(s1, s2, t1, t2)
```,caption: [`random_move` + `random_moves_without_replacement` method implemented to be used by improvement methods which deliberately takes worse choices to escape local optima's]
)<rand>
The `random_move` (@rand) iterates over the ordered pairs $(s_1, s_2)$ where $s_1 != s_2$ as given from the `sparse_fisher_yates_iter` method. This way the `random_moves_without_replacement` method can decode each iteration back to two different students. This works since the shuffle works over the total of $abs(S) dot abs(S)$. Roughly half the indices are discarded (where s1 ≥ s2), so there might exist some more efficient methods of encoding, but the simplicity of this approach works just fine for this project.

#codly(offset-from: <rand>)
#figure(
  ```py
def sparse_fisher_yates_iter(n: int) -> Iterable[int]:
    p: dict[int, int] = dict()
    for i in range(n - 1, -1, -1):
        r = random.randrange(i + 1)
        yield p.get(r, r)
        if i != r:
            p[r] = p.get(i, i)
```,caption: [The `sparse_fisher_yates_iter` method implemented for effective shuffling]
)<fisheryates>
The `sparse_fisher_yates_iter` (@fisheryates) method is used here to shuffle the set of teams, such that the `random_moves_without_replacement` method can randomly assign students to teams. It does this by randomly selecting a number from the range `n-1`, keeping track of seen numbers with a `dict()` 


=== Swap team moves
The following methods should implement the behavior of two student $s_1$ and $s_2$ swapping teams $T_1$ and $T_2$. More formally
$ m(s, t_"from", t_"to") : sigma(s) = t_"from" arrow sigma(s) = t_"to" $
#figure(
  ```py
class SwapMove(...):
    def __init__(self, student1: int, student2: int, team1: int, team2: int):
        self.s1 = student1
        self.s2 = student2
        self.t1 = team1
        self.t2 = team2
        
    def apply_move(self, solution: Solution) -> Solution:
        prob = solution.problem
        solution.lb += self.objective_value_increment(solution)

        # s1 leaves t1, joins t2
        for a, label in enumerate(prob.attributes[self.s1]):
            from_counts = solution.team_labels[self.t1][a]
            from_counts[label] -= 1
            if from_counts[label] == 0:
                del from_counts[label]
            to_counts = solution.team_labels[self.t2][a]
            to_counts[label] = to_counts.get(label, 0) + 1
        solution.assignments[self.s1] = self.t2
```,caption: [Part of the `apply_move` method that re-assigns student 1 $s_1$ to their new team]
)<swap1>

Firstly $s_1$ leaves $T_1$ and joins $T_2$, such that both teams are updated. Here their label-count is updated trough the references `from_counts` and `from_counts` corresponding to the team $s_1$ is coming from and going to. Then in the end, the actual assignment is made
#codly(offset-from: <swap1>)
#figure(
  ```py
        # s2 leaves t2, joins t1
        for a, label in enumerate(prob.attributes[self.s2]):
            from_counts = solution.team_labels[self.t2][a]
            from_counts[label] -= 1
            if from_counts[label] == 0:
                del from_counts[label]
            to_counts = solution.team_labels[self.t1][a]
            to_counts[label] = to_counts.get(label, 0) + 1
        solution.assignments[self.s2] = self.t1
        return solution
```,caption: [Part of the `apply_move` method that re-assigns student 2 $s_2$ to their new team]
)<swap2>
The exact same is done to $s_2$ (@swap2).

The increment (@incswap) should then also resemble the swap such that, its updated with respect the the weights and labels in the two teams
#figure(
  ```py
def score_increment(self, solution: Solution) -> float:
        prob = solution.problem
        from_counts = solution.team_labels[self.fromTeam]
        to_counts = solution.team_labels[self.toTeam]
        s_labels = prob.attributes[self.s]
        incr = 0
        for a, label in enumerate(s_labels):
            # s leaves fromTeam: lb drops if s was the last holder of this label
            if from_counts[a].get(label, 0) == 1:
                incr -= prob.weights[a]
            # s joins toTeam: lb rises if toTeam has no holder of this label yet
            if to_counts[a].get(label, 0) == 0:
                incr += prob.weights[a]
        return incr
```, caption: [Score incrementation implemented for the `SwapMove` method]
)<incswap>
For task 3 the constructed solutions from task 2 is tested and improved upon on 2 different solvers, that is the `best_improvement` and the `first_improvement`. 

=== Testing and comparison
Now lets some different improvement algorithms on this swap move. This test will include `best_improvement` and `first_improvement` These algorithms are simple local search heuristics that serve as useful baselines before introducing more advanced meta-heuristics later (Task 4). The `first_improvement` algorithm applies the first improving move it encounters, while `best_improvement` evaluates all improving moves and selects the best one. This will compare on the  `greedy_construction` from earlier since, it proved itself most competitive.

#figure(```output
Is feasible: True
Solution(
  cost=68770
)
Execution time: 0.996727705001831
Is feasible: True
Solution(
  cost=7240
)
Execution time: 22.735021829605103
```, caption: [Output of the `best_improvement` method improving on the `greedy_construction` method on 300 students]
)<bestimprovment>
The `best_improvement` (@bestimprovment) is a remarkable improvement of almost $apx 90%$ lower objective value. Though it came with a cost of almost 23 seconds to compute. Note that `best_improvement` is $sans(O(n^2))$ so given this large instance of 300 students that $approx 90000$ indices pr. iteration. because of this it's expected and acceptable that it takes some time.
Lets take a look at the first improvement.

#figure(
  ```output
Is feasible: True
Solution(
  cost=68770
)
Execution time: 0.9894468784332275
Is feasible: True
Solution(
  cost=7430
)
Execution time: 1.604125738143921
```, caption: [Output of the `first_improvement` method improving on the `greedy_construction` method on 300 students]
)<firstimprovement>
The `first_improvement` (@firstimprovement) did almost the same improvement of $apx 89%$ lower objective value in roughly $apx 6%$ of the time. This suggests that the neighbourhood in this instance is relatively “easy” in the sense that good improving moves are found quickly, often early in the neighbourhood. In such a setting, first-improvement benefits from avoiding a full neighbourhood evaluation, while still reaching comparable local optima. In contrast, `best_improvement` is more sensitive to this structure, as it evaluates all moves even when good improvements are already available early.



#pagebreak()
== Task 4 - meta-heuristics

For this task, several meta-heuristic algorithms could be explored. Simulated Annealing (SA) is selected here, as it is good for escaping local optima by probabilistically accepting worsening moves, and so makes it well suited for this problem. Besides this it creates the opportunity to experiment with cooling schedules and their effect on solution quality, which the group finds of much interest.

The SA uses the Metropolis condition 
$ p = exp((-Delta)/T_i) $
Where $Delta$ is the cost increase, and $T_i$ is the current temperature. This criteria ensures a move that worsens the solution by Δ is accepted with a probability of $exp((-Delta)/T_i)$. Then for the initial  temperature, one can just fix a probability of $50%$. $Delta$ can be approximated by running a series objective values on some of random moves.

#figure(
  ```py
def estimate_delta(neighbourhood, solution, n_samples) -> float:
    deltas = []
    for _ in range(n_samples):
        move = neighbourhood.random_move(solution)
        if move is None:
            break
        incr = move.objective_value_increment(solution)
        print(incr)
        if incr > 0:
            deltas.append(incr)
    return sum(deltas) / len(deltas) if deltas else 1.0
```,caption: [Estimating the average deltas of the move increment of 100 random moves]
)<deltas>
With a quick test (@deltas) the average delta of 100 random iterations is set to 1. This means that before SA even begins there a almost only acceptable moves, because the 

Then $T_0$ can be calculated as $ T_0 = (-1)/ln(0.5) apx 3.32  $
Once this is done, the different temperature schedulers can be explored. Lets look at `geometric` and `cosineRestarts` @divedeep

=== Geometric decay scheduler
The geometric decay scheduler (@geocode), also known as factor decay, applies a constant decay factor at each iteration making a polynomial smooth decay.
$ T_(i+1) = alpha dot T_(i) where alpha in [0,1] $
#figure(
  ```py
def geometric(t0: float, cooling: float = 0.999) -> Callable[[int], float]:
    def schedule(k: int) -> float:
        return t0 * (cooling ** k)
    return schedule
```,caption: [Geometric (factor) decay implemented for the simulated annealing method]
)<geocode>

=== Cosine scheduler
Now to implement a completely different decay scheduler; The Cosine Decay.
$ T_(i) = T_"min" + (T_0 - T_"min")/2 (1 dot cos((pi i)/i_"max")) where i = 1,2,dots n "iterations." $
The cosine decay scheduler (@coscode) follows the same formular as presented above, decaying from an initial temperature $t_0$ down to the minimum temperature $t_min$ with a cosine curve. This can be favorable since is spends more iterations being warm, and only cooling at the end. This supports the procces that the most important places to allow worse decisions might be in the beginning.
#figure(
  ```py
def cosine(t0: float, t_min: float = 1.0, total: int = 1_000_000) ->
                                        Callable[[int], float]:
    def schedule(k: int) -> float:
        progress = min(k / total, 1.0)
        return t_min + 0.5 * (t0 - t_min) * (1 + math.cos(math.pi * progress))
    return schedule
```, caption: [Cosine decay implemented for the simulated annealing method.]
)<coscode>
=== Simulated annealing 
#figure(
  ```py
  def sa(problem, solution: Solution,budget: float = 60.0,
    p_accept: float = 0.5, scheduler: Callable[[int], float] = None,
    record: bool = False) -> tuple[Solution, list] | Solution:
    """
    Simulated Annealing (SA), using a scheduler, for the assignment problem implemented using `ROAR-NET-API`
    """

    neighbourhood = problem.local_neighbourhood()
    s = solution.copy_solution()
    best = s.copy_solution()

    delta = estimate_delta(neighbourhood, s)
    t0 = -delta / math.log(p_accept)
    if scheduler is None:
        scheduler = geometric(t0)

    history = []
    t_start = time.time()
    k = 0
    while time.time() - t_start < budget:
        move = neighbourhood.random_move(s)
        if move is None:
            break
        incr = move.objective_value_increment(s)
        temp = scheduler(k)
        if temp == 0:
            break
        accepted = incr < 0 or random.random() < math.exp(-incr / temp)
        if accepted:
            move.apply_move(s)
            if s.lb < best.lb:
                best = s.copy_solution()
        if record:
            history.append({"k": k, "temp": temp, "cost": s.lb})
        k += 1

    return (best, history) if record else best
  ```
)
The simulated annealing method above finds a best solution, within a time interval (constrained by the decay). It initiates a $Delta$ value with the `estimate_delta`, and  creates random moves within the time interval, selecting better moves along the way. The simulated annealing method escapes local optima by sometimes taking bad moves. This is done at line `28`, where a move is accepted if the increment is smaller (e.i. the move is better), or at random times given the scheduler allows it.

#pagebreak()
=== Testing
Now lets test both of the schedulers to see their performance on this problem.

#figure(
  image("assets/geometric.png"),
  caption: [Here is the simulated annealing depicted with a geometric scheduler. The upper figure shows the temperature decreasing by a constant factor, and lower figure shows the cost dropping accordingly]
)<geo>
#figure(
  image("assets/cosine.png"),
  caption: [Here is the simulated annealing depicted with a cosine scheduler. The upper figure shows the temperature decreasing with a cosine shape, and the lower figure shows  cost dropping accordingly]
)<cos>
As shown on @geo and @cos, both schedulers can be visualized to verify expected behavior. @geo shows the geometric scheduler decaying rapidly toward zero, while @cos shows the cosine scheduler cooling gradually.

#pagebreak()
For testing, one can do iterative restarts on the simulated annealing method. This means doing multiple runs of simulated annealing and updating the best of the solutions. In the following example, the simulated annealing algorithm was run *10 times*. because of this, the execution time also reflects this.
#figure(
  ```output
Is feasible: True
Solution(
  cost=68770
)
Execution time: 1.0040440559387207
Is feasible: True
Solution(
  cost=6660
)
Execution time: 358.7554180622101
```,caption: [Solution made by simulated annealing with a geometric scheduler]
)<geo2>

#figure(
  ```output
Is feasible: True
Solution(
  cost=68770
)
Execution time: 0.9936981201171875
Is feasible: True
Solution(
  cost=6800
)
Execution time: 622.6760261058807
```, caption: [Solution made by simulated annealing with a cosine scheduler]
)<cos2>
The simulated annealing methods (@geo2 and @cos2), improves even further on the solution, and results in a better solution than both the `best_improvement` and `first_improvement`. The best  result of the simulated annealing methods resulted in a best solution of `cost=6660`. This came using the geometric scheduler. Note that all results from Case 2, are tested on a Mac Book Air 15, with an apple M4 chip and 16 GB ram.

== Conclusion on Case 2
The results from the case 2 experiments has shown that the implemented methods to be a valuable the optimization process. The greedy construction heuristic reliably produces complete, feasible solutions. The local search improvement methods showed significantly better solutions compared to the constructed ones. The simulated annealing proved to be the most effective approach overall, being able to escape local optima through somewhat controlled randomness. It achieved the overall lowest solution costs within what the authors view as an acceptable computational time. The best solution achieved with the simulated annealing using a geometric scheduler achieved the low cost of `6660`.
The implemented methods overall each create a distinct role in the optimization process, and offers different trade-offs between solution quality and computational effort.

// ─── Appendix ─────────────────────────────────────────────────────────────────
#pagebreak()
#bib("references.bib")
